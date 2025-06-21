from django.urls import path
from . import views


urlpatterns = [
    path('', views.VideoListView.as_view(), name='home'),
    path('videos/<int:video_id>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('videos/<int:video_id>/delete/', views.VideoDeleteView.as_view(), name='video_delete'),
]