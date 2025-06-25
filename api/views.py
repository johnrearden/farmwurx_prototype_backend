from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from video_management.models import VideoRawUpload
from api.serializers import VideoRawUploadSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class VideoUploadAPIView(ListCreateAPIView):
    """
    View to handle video uploads.
    This view will be used to upload raw videos.
    """
    permission_classes = [IsAuthenticated]
    queryset = VideoRawUpload.objects.all()
    serializer_class = VideoRawUploadSerializer

    def perform_create(self, serializer):
        """
        Override to set the user from the request.
        """
        serializer.save(user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePushNotificationTokenAPIView(APIView):
    """
    View to update the push notification token.
    This view will be used to update the user's push notification token.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to update the push notification token.
        """
        token = request.data.get('token')
        if not token:
            return render(request, 'error.html', {'message': 'Token is required.'})
        
        # Update the user's push notification token
        request.user.push_notification_token = token
        request.user.save()
        
        return Response({'message': 'Token updated successfully.'})
