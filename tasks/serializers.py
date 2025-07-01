from .models import Task
from video_management.serializers import VideoRawUploadSerializer
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    This serializer is used to convert Task instances to JSON format and vice versa.
    """

    tasker_name = serializers.ReadOnlyField(source='tasker.username')
    taskee_name = serializers.ReadOnlyField(source='taskee.username')
    video = VideoRawUploadSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'tasker', 'taskee', 'description',
            'created_at', 'updated_at', 'due_date', 'video'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', ]
    
    def create(self, validated_data):
        """
        Create a new Task instance.
        This method is called when a new task is created.
        """
        return Task.objects.create(**validated_data)