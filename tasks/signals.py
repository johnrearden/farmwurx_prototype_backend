from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from video_management.models import VideoRawUpload
from video_management.tasks import process_uploaded_video
import os
import logging
logger = logging.getLogger('django')


@receiver(post_save, sender=Task)
def process_video_on_task_creation(sender, instance, created, **kwargs):
    """
    Signal to process video when a task is created.
    This will trigger the video processing task if the task is associated with a video.
    """
    if created and instance.video:
        try:
            # Trigger the video processing task
            process_uploaded_video.delay(
                video_id=instance.video.id,
                taskee_id=instance.taskee.id,
            )
        except Exception as e:
            logger.error(f"Error processing video for task {instance.id}: {e}")
            # Optionally, you can handle the error further, e.g., notify admins or retry
                