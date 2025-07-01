from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import VideoRawUpload
from django.views import View
from .forms import TaskForm
from tasks.models import Task


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
        
        return redirect('video_list')


class CreateTaskFromVideoView(View):
    """
    View to create a task from a video.
    """
    def get(self, request, video_id):
        """
        Handle GET requests to display the task creation form.
        """
        video = get_object_or_404(VideoRawUpload, id=video_id)
        
        # Initialize the form with default values
        initial_data = {
            'include_video': True,
            'include_transcription': bool(video.transcription),
        }
        
        # If video has transcription and include_transcription is True, 
        # use it as initial description
        if video.transcription:
            initial_data['description'] = video.transcription[:500] + ('...' if len(video.transcription) > 500 else '')
        
        form = TaskForm(initial=initial_data)
        
        return render(
            request,
            'video_management/create_task.html',
            {
                'form': form,
                'video': video,
            }
        )
    
    def post(self, request, video_id):
        """
        Handle POST requests to create a task.
        """
        video = get_object_or_404(VideoRawUpload, id=video_id)
        form = TaskForm(request.POST)
        
        if form.is_valid():
            # Create a new task with current user as tasker
            task = Task(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                tasker=request.user,  # Current user as task creator
                taskee=form.cleaned_data['taskee'],  # Selected user from dropdown
                due_date=form.cleaned_data['due_date'],
            )
            
            # Link video if requested
            if form.cleaned_data.get('include_video'):
                task.video = video
                
            # Save the task
            task.save()
            
            messages.success(request, "Task created successfully!")
            return redirect('task_detail', task_id=task.id)
        
        # If form is invalid, redisplay with errors
        return render(
            request,
            'video_management/create_task.html',
            {
                'form': form,
                'video': video,
            }
        )
