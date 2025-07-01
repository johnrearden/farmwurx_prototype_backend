from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This allows for future extensibility without changing the default user model.
    """
    USER_TYPE_CHOICES = {
        "ADMIN": "Admin",
        "SUPER": "Supervisor",
        "STAFF": "Staff",
    }
    push_notification_token = models.CharField(
        max_length=255, blank=True, null=True, help_text="Token for push notifications"
    )
    user_type = models.CharField(
        max_length=10,
        choices=[(key, value) for key, value in USER_TYPE_CHOICES.items()],
        default="STAFF",
        help_text="Type of user for role-based access control"
    )
    main_language = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Main language of the user, used for transcription and captioning"
    )
    secondary_language = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Secondary language of the user, used for transcription and captioning"
    )
    
    def __str__(self):
        return self.username
