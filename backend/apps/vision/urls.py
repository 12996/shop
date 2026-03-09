from django.urls import path

from .views import RecognizeView


urlpatterns = [
    path("admin/vision/recognize", RecognizeView.as_view(), name="vision-recognize"),
]
