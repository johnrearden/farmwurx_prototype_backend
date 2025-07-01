from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Task
import requests
import logging
logger = logging.getLogger("django")

User = get_user_model()

class TaskListView(View):
    """
    View to display all tasks with optional filtering by taskee.
    """
    def get(self, request):
        """
        Handle GET requests to list tasks.
        """
        # Get the taskee filter parameter from the URL
        taskee_id = request.GET.get('taskee')
        
        # Base queryset
        tasks = Task.objects.all().order_by('-created_at')
        
        # Apply filter if provided
        if taskee_id:
            try:
                tasks = tasks.filter(taskee_id=int(taskee_id))
                selected_taskee = User.objects.get(id=taskee_id)
            except (ValueError, User.DoesNotExist):
                selected_taskee = None
        else:
            selected_taskee = None
            
        # Get all users for the filter dropdown
        users = User.objects.all()
        
        context = {
            'tasks': tasks,
            'users': users,
            'selected_taskee': selected_taskee,
        }
        
        return render(request, 'tasks/task_list.html', context)

class TaskDetailView(View):
    """
    View for displaying task details.
    """
    def get(self, request, task_id):
        """
        Handle GET requests to display task details.
        """
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'tasks/task_detail.html', {'task': task})


class TaskDeleteView(View):
    """
    View for deleting a task.
    """
    def post(self, request, task_id):
        """
        Handle POST requests to delete a task.
        """
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        messages.success(request, "Task successfully deleted.")
        return redirect('task_list')
    

class TaskResendView(View):
    """
    View for resending a task.
    """
    def post(self, request, task_id):
        """
        Handle POST requests to resend a task.
        """
        task = get_object_or_404(Task, id=task_id)
        EXPO_PUSH_ENDPOINT = "https://exp.host/--/api/v2/push/send"

        taskee = task.taskee
        video_raw_upload = task.video
        try:
            # Notify the client that the video and vtt file are ready
            expo_token = taskee.push_notification_token
            message = {
                "to": expo_token,
                "sound": "default",
                "title": "Video Ready!",
                "body": "You have a new task video with captions!",
                "data": {
                    "action": "video_ready",
                    "video_id": video_raw_upload.id,
                    "video_url": video_raw_upload.video.url,
                    "vtt_url": video_raw_upload.vtt_file.url
                },
                "priority": "high",
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
            }

            response = requests.post(EXPO_PUSH_ENDPOINT, json=message, headers=headers)
            logger.info(f"Expo push notification response: {response.status_code} - {response.text}")
            response.raise_for_status()

        except Exception as e:
            logger.error(f"Error sending push notification: {e}")
        
        # Logic to resend the task (e.g., reassigning or notifying)
        # This is a placeholder; actual implementation may vary
        messages.success(request, f"Task '{task.name}' has been resent.")
        
        return redirect('task_list')
