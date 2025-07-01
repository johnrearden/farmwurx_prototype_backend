from django.apps import AppConfig


class VideoManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_management'

    def ready(self):
        import video_management.signals  # Ensure signals are imported when the app is ready
