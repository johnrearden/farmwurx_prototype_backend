from django.urls import path
from .views import VideoUploadAPIView, UpdatePushNotificationTokenAPIView   


urlpatterns = [
    path('upload_video/', VideoUploadAPIView.as_view(), name='video-upload'),
    path(
        'update_push_notification_token/',
        UpdatePushNotificationTokenAPIView.as_view(),
        name='update-push-notification-token'
    ),
]