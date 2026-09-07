

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: replace this before deploying anywhere public.
SECRET_KEY = "django-insecure-change-this-before-you-deploy-anywhere-real"

# SECURITY WARNING: don't run with DEBUG turned on in production.
DEBUG = True

ALLOWED_HOSTS: list[str] = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "remover",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bgremover_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "bgremover_site.wsgi.application"

# A local sqlite database is included only because Django's session
# middleware expects one to exist. The app itself doesn't store anything.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "remover" / "static"]

# Uploaded images are processed in memory and never written to disk,
# so no MEDIA_ROOT is needed.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- App-specific settings -------------------------------------------------

# Largest upload Matte will accept, in bytes.
MATTE_MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

# rembg model used per "cut quality" option exposed in the UI.
MATTE_MODELS = {
    "fast": "u2netp",
    "balanced": "u2net",
    "precise": "isnet-general-use",
}
DATA_UPLOAD_MAX_MEMORY_SIZE = MATTE_MAX_UPLOAD_BYTES + 1024 * 1024
