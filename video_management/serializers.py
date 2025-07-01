from .models import VideoRawUpload
from rest_framework import serializers


class VideoRawUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for VideoRawUpload model.
    This serializer is used to convert VideoRawUpload instances to JSON format and vice versa.
    """
    video_server_url = serializers.ReadOnlyField(source='video.url')
    thumbnail_server_url = serializers.ReadOnlyField(source='thumbnail.url')
    vtt_server_url = serializers.ReadOnlyField(source='vtt_file.url')
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = VideoRawUpload
        fields = [
            'id', 'user', 'user_name', 'video', 'video_server_url', 
            'thumbnail', 'thumbnail_server_url', 'vtt_file',
            'vtt_server_url', 'uploaded_at', 'file_size', 'transcription', 
        ]

    def create(self, validated_data):
        """
        Create a new VideoRawUpload instance.
        This method is called when a new video upload is created.
        """
        return VideoRawUpload.objects.create(**validated_data)