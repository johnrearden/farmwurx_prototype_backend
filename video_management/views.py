from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import VideoRawUpload
from django.views import View


class VideoListView(View):
    """
    View to list all uploaded videos.
    This view will be used to display a list of all uploaded videos.
    """
    def get(self, request):
        """
        Handle GET requests to list videos.
        """
        videos = VideoRawUpload.objects.all()
        return render(request, 'video_management/video_list.html', {'videos': videos})


class VideoDetailView(View):
    """
    View to display details of a specific video.
    """
    def get(self, request, video_id):
        """
        Handle GET requests to display video details.
        """
        video = get_object_or_404(VideoRawUpload, id=video_id)
        return render(
            request,
            'video_management/video_detail.html',
            {'video': video}
        )
    
    
class VideoDeleteView(View):
    """
    View to delete a video.
    """
    def post(self, request, video_id):
        """
        Handle POST requests to delete a video.
        """
        video = get_object_or_404(VideoRawUpload, id=video_id)
        
        # Optional: Check if user has permission to delete this video
        # if video.user != request.user and not request.user.is_staff:
        #     messages.error(request, "You don't have permission to delete this video.")
        #     return redirect('video_list')
        
        # Delete the video
        video.delete()
        messages.success(request, "Video successfully deleted.")
        
        return redirect('home')
