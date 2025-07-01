from django.urls import path
from . import views


urlpatterns = [
    path('', views.VideoListView.as_view(), name='video_list'),  # Empty path points to video_list
    path('videos/<int:video_id>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('videos/<int:video_id>/delete/', views.VideoDeleteView.as_view(), name='video_delete'),
    path('videos/<int:video_id>/create-task/', views.CreateTaskFromVideoView.as_view(), name='create_task_from_video'),
]