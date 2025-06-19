from django.urls import path
from .views import VideoUploadAPIView


urlpatterns = [
    path('videos/', VideoUploadAPIView.as_view(), name='video-upload'),
]