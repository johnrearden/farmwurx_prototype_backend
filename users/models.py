from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This allows for future extensibility without changing the default user model.
    """
    # You can add additional fields here if needed
    # For example:
    # bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username
