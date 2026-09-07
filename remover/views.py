import base64
import io

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from PIL import Image, UnidentifiedImageError

# rembg loads a fair amount on first import (onnxruntime, numpy, etc.),
# so it's imported lazily inside cut_image rather than at module load.
# Sessions are cached per model name so the underlying network weights
# are only loaded once per process, not once per request.
_SESSIONS: dict[str, object] = {}


def _get_session(model_name: str):
    if model_name not in _SESSIONS:
        from rembg import new_session

        _SESSIONS[model_name] = new_session(model_name)
    return _SESSIONS[model_name]


@require_GET
def index(request):
    return render(
        request,
        "remover/index.html",
        {
            "max_upload_mb": settings.MATTE_MAX_UPLOAD_BYTES // (1024 * 1024),
        },
    )


@require_POST
def cut_image(request):
    upload = request.FILES.get("image")
    if upload is None:
        return JsonResponse({"error": "No file came through. Try choosing a photo again."}, status=400)

    if upload.size > settings.MATTE_MAX_UPLOAD_BYTES:
        limit_mb = settings.MATTE_MAX_UPLOAD_BYTES // (1024 * 1024)
        return JsonResponse(
            {"error": f"That file's too big — try something under {limit_mb}MB."},
            status=400,
        )

    quality = request.POST.get("quality", "balanced")
    model_name = settings.MATTE_MODELS.get(quality, settings.MATTE_MODELS["balanced"])

    raw_bytes = upload.read()

    # Confirm this is actually a readable image before handing it to the model.
    try:
        probe = Image.open(io.BytesIO(raw_bytes))
        probe.verify()
    except (UnidentifiedImageError, OSError):
        return JsonResponse(
            {"error": "This isn't an image Matte can read — try a JPG or PNG."},
            status=400,
        )

    try:
        from rembg import remove

        session = _get_session(model_name)
        output_bytes = remove(raw_bytes, session=session)
    except Exception:
        return JsonResponse(
            {"error": "The cut didn't go through on that image. Try a different photo."},
            status=500,
        )

    encoded = base64.b64encode(output_bytes).decode("ascii")
    return JsonResponse({"result": f"data:image/png;base64,{encoded}"})
