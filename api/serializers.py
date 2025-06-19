from rest_framework import serializers
from video_management.models import VideoRawUpload


class VideoRawUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for VideoRawUpload model.
    """
    class Meta:
        model = VideoRawUpload
        fields = ['id', 'user', 'video', 'uploaded_at']
        read_only_fields = ['id', 'user', 'uploaded_at']

    def create(self, validated_data):
        """
        Create a new VideoRawUpload instance.
        """
        return VideoRawUpload.objects.create(**validated_data)