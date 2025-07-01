import os
from django.db import models
from django.conf import settings

class VideoRawUpload(models.Model):
    """
    Model to store raw video uploads.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='raw_videos'
    )
    video = models.FileField(upload_to='raw_videos/')
    audio = models.FileField(upload_to='extracted_audio/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(null=True, blank=True)  # Duration in seconds
    file_size = models.BigIntegerField(null=True, blank=True)  # Size in bytes
    audio_extraction_duration = models.FloatField(null=True, blank=True)  # Duration of audio extraction in seconds
    audio_transcription_duration = models.FloatField(null=True, blank=True)  # Duration of transcription in seconds
    transcription = models.TextField(blank=True, null=True)  # Transcription of the audio
    vtt_file = models.FileField(
        upload_to='captions/',
        blank=True,
        null=True,
        help_text="WebVTT file for the transcription"
    )

    def __str__(self):
        return f"Raw Video {self.id} - {self.uploaded_at}"
    
    def save(self, *args, **kwargs):
        # Calculate file size if video exists and is a new file
        if self.video and hasattr(self.video, 'size') and not self.file_size:
            self.file_size = self.video.size
        super().save(*args, **kwargs)



