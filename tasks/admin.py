from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):    
    """
    Admin interface for managing tasks.
    """
    list_display = ('name', 'tasker', 'taskee', 'created_at', 'due_date')
    search_fields = ('name', 'tasker__username', 'taskee__username')
    list_filter = ('created_at', 'due_date', 'tasker', 'taskee')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'