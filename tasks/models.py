from django.db import models
from django.conf import settings


class Task(models.Model):
    """
    Model to represent a task in the system.
    """
    name = models.CharField(max_length=255, help_text="Name of the task")
    tasker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="User who is assigned to the task"
    )
    taskee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        help_text="User who is responsible for completing the task"
    )
    description = models.TextField(blank=True, null=True, help_text="Description of the task")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the task was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the task was last updated")
    due_date = models.DateTimeField(blank=True, null=True, help_text="Due date for the task completion")
    video = models.ForeignKey(
        'video_management.VideoRawUpload',
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="Video associated with the task"
    )

    def __str__(self):
        return self.name
