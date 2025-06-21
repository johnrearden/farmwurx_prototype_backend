import os
import time
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from moviepy import VideoFileClip

from .utils import transcribe_audio, write_webvtt

class VideoRawUpload(models.Model):
    """
    Model to store raw video uploads.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='raw_videos'
    )
    video = models.FileField(upload_to='raw_videos/')
    audio = models.FileField(upload_to='extracted_audio/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(null=True, blank=True)  # Duration in seconds
    file_size = models.BigIntegerField(null=True, blank=True)  # Size in bytes
    audio_extraction_duration = models.FloatField(null=True, blank=True)  # Duration of audio extraction in seconds
    audio_transcription_duration = models.FloatField(null=True, blank=True)  # Duration of transcription in seconds
    transcription = models.TextField(blank=True, null=True)  # Transcription of the audio
    vtt_file = models.FileField(
        upload_to='captions/',
        blank=True,
        null=True,
        help_text="WebVTT file for the transcription"
    )

    def __str__(self):
        return f"Raw Video {self.id} - {self.uploaded_at}"
    
    def save(self, *args, **kwargs):
        # Calculate file size if video exists and is a new file
        if self.video and hasattr(self.video, 'size') and not self.file_size:
            self.file_size = self.video.size
        super().save(*args, **kwargs)


@receiver(post_save, sender=VideoRawUpload)
def process_video(sender, instance, created, **kwargs):
    """
    Process video after upload - extract audio, generate thumbnail, etc.
    """
    if created and instance.video:
        try:
            # Get the video path
            video_path = instance.video.path
            
            # Open the video
            clip = VideoFileClip(video_path)
            
            # Set the duration
            if not instance.duration:
                instance.duration = clip.duration
            
            # Extract audio if not already done
            if not instance.audio:
                # Create audio filename
                start_time = time.perf_counter()
                base_name = os.path.splitext(os.path.basename(video_path))[0]
                audio_path = os.path.join(
                    settings.MEDIA_ROOT,
                    'extracted_audio',
                    f"{base_name}.mp3"
                )
                
                # Make sure directory exists
                os.makedirs(os.path.dirname(audio_path), exist_ok=True)
                
                # Extract audio
                clip.audio.write_audiofile(audio_path)
                instance.audio_extraction_duration = time.perf_counter() - start_time

                # Create transcription
                start_time_transcription = time.perf_counter()
                transcription, segments_list, info = transcribe_audio(audio_path)
                
                instance.transcription = transcription
                time_elapsed = time.perf_counter() - start_time_transcription
                instance.audio_transcription_duration = time_elapsed

                # Write WebVTT file
                vtt_path = os.path.join(
                    settings.MEDIA_ROOT,
                    'captions',
                    f"{base_name}.vtt"
                )
                write_webvtt(segments_list, output_path=vtt_path)
                
                # Verify VTT file was created and has content
                if os.path.exists(vtt_path) and os.path.getsize(vtt_path) > 0:
                    print(f"VTT file created successfully at {vtt_path}, size: {os.path.getsize(vtt_path)} bytes")
                    instance.vtt_file = os.path.relpath(vtt_path, settings.MEDIA_ROOT)
                else:
                    print(f"Warning: VTT file at {vtt_path} is empty or was not created")
                
                # Save the relative path to the model
                relative_path = os.path.relpath(audio_path, settings.MEDIA_ROOT)
                instance.audio = relative_path
            
            # Generate thumbnail if not already done
            if not instance.thumbnail:
                # Create thumbnail filename
                base_name = os.path.splitext(os.path.basename(video_path))[0]
                thumbnail_path = os.path.join(
                    settings.MEDIA_ROOT,
                    'thumbnails',
                    f"{base_name}.jpg"
                )
                
                # Make sure directory exists
                os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
                
                # Take frame at 2 seconds (or the middle if shorter)
                if clip.duration <= 4:
                    frame_time = clip.duration / 2
                else:
                    frame_time = 2
                
                # Save the thumbnail
                clip.save_frame(thumbnail_path, t=frame_time)
                
                # Save the relative path to the model
                relative_path = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT)
                instance.thumbnail = relative_path
            
            # Close the clip to free resources
            clip.close()
            
            # Save the instance with the new data
            instance.save()
                
        except Exception as e:
            print(f"Error processing video: {e}")
            import traceback
            traceback.print_exc()


@receiver(pre_delete, sender=VideoRawUpload)
def delete_video_files(sender, instance, **kwargs):
    """
    Delete all files associated with the video before deleting the model instance.
    """
    try:
        # Delete the video file
        if instance.video and hasattr(instance.video, 'path') and os.path.exists(instance.video.path):
            print(f"Deleting video file: {instance.video.path}")
            instance.video.delete(save=False)
        
        # Delete the audio file
        if instance.audio and hasattr(instance.audio, 'path') and os.path.exists(instance.audio.path):
            print(f"Deleting audio file: {instance.audio.path}")
            instance.audio.delete(save=False)
        
        # Delete the thumbnail
        if instance.thumbnail and hasattr(instance.thumbnail, 'path') and os.path.exists(instance.thumbnail.path):
            print(f"Deleting thumbnail file: {instance.thumbnail.path}")
            instance.thumbnail.delete(save=False)
        
        # Delete the VTT file
        if instance.vtt_file and hasattr(instance.vtt_file, 'path') and os.path.exists(instance.vtt_file.path):
            print(f"Deleting VTT file: {instance.vtt_file.path}")
            instance.vtt_file.delete(save=False)
        
    except Exception as e:
        print(f"Error deleting video files: {e}")
        import traceback
        traceback.print_exc()
