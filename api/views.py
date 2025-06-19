from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from video_management.models import VideoRawUpload
from api.serializers import VideoRawUploadSerializer


class VideoUploadAPIView(CreateAPIView):
    """
    View to handle video uploads.
    This view will be used to upload raw videos.
    """
    permission_classes = [IsAuthenticated]
    queryset = VideoRawUpload.objects.all()
    serializer_class = VideoRawUploadSerializer

    def perform_create(self, serializer):
        """
        Override to set the user from the request.
        """
        serializer.save(user=self.request.user)
