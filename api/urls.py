from django.urls import path
from .views import VideoUploadAPIView


urlpatterns = [
    path('upload_video/', VideoUploadAPIView.as_view(), name='video-upload'),
]