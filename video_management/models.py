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
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Raw Video {self.id} - {self.uploaded_at}"
