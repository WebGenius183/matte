from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("", include("remover.urls")),
]

urlpatterns += staticfiles_urlpatterns()
