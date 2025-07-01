from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import VideoRawUpload
from .tasks import process_uploaded_video
import os

@receiver(post_save, sender=VideoRawUpload)
def process_video(sender, instance, created, **kwargs):
    if created and instance.video:
        process_uploaded_video.delay(instance.id)


@receiver(pre_delete, sender=VideoRawUpload)
def delete_video_files(sender, instance, **kwargs):
    try:
        if instance.video and hasattr(instance.video, 'path') and os.path.exists(instance.video.path):
            instance.video.delete(save=False)
        if instance.audio and hasattr(instance.audio, 'path') and os.path.exists(instance.audio.path):
            instance.audio.delete(save=False)
        if instance.thumbnail and hasattr(instance.thumbnail, 'path') and os.path.exists(instance.thumbnail.path):
            instance.thumbnail.delete(save=False)
        if instance.vtt_file and hasattr(instance.vtt_file, 'path') and os.path.exists(instance.vtt_file.path):
            instance.vtt_file.delete(save=False)
    except Exception as e:
        import traceback
        print(f"Error deleting video files: {e}")
        traceback.print_exc()