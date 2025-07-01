from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('<int:task_id>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('resend/<int:task_id>/', views.TaskResendView.as_view(), name='task_resend'),
]
