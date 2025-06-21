from rest_framework import serializers
from video_management.models import VideoRawUpload


class VideoRawUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for VideoRawUpload model.
    """
    class Meta:
        model = VideoRawUpload
        fields = ['id', 'user', 'video', 'audio', 'uploaded_at']
        read_only_fields = [
            'id', 'user', 'uploaded_at', 'audio', 'audio_extracted',
            'extraction_error'
        ]

    def create(self, validated_data):
        """
        Create a new VideoRawUpload instanceand extract audio synchronously.
        This method is called when a new video upload is created.
        """

        # Return the created instance
        return VideoRawUpload.objects.create(**validated_data)