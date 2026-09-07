from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cut/", views.cut_image, name="cut_image"),
]
