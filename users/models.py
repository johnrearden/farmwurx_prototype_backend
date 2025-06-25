from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This allows for future extensibility without changing the default user model.
    """
    push_notification_token = models.CharField(
        max_length=255, blank=True, null=True, help_text="Token for push notifications"
    )
    
    def __str__(self):
        return self.username
