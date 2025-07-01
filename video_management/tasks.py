import os
import time
import requests
from django.conf import settings
from celery import shared_task
from .models import VideoRawUpload
from .utils import (
    transcribe_audio, translate_text, write_webvtt
)
from moviepy import VideoFileClip


EXPO_PUSH_ENDPOINT = "https://exp.host/--/api/v2/push/send"


@shared_task
def process_uploaded_video(video_id):
    instance = VideoRawUpload.objects.get(id=video_id)
    if not instance.video:
        raise ValueError("No video file found for the provided video ID.")
    
    video_path = instance.video.path
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    try:
        clip = VideoFileClip(video_path)
        instance.duration = clip.duration

        if not instance.audio:
            # Extract audio
            start = time.perf_counter()
            audio_path = os.path.join(
                settings.MEDIA_ROOT,
                'extracted_audio',
                f"{base_name}.mp3"
            )
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            clip.audio.write_audiofile(audio_path)
            instance.audio_extraction_duration = time.perf_counter() - start

            # Transcribe audio
            start_transcription = time.perf_counter()
            transcription, segments_list, _ = transcribe_audio(audio_path)
            instance.transcription = transcription
            instance.audio_transcription_duration = (
                time.perf_counter() - start_transcription
            )

            for s in segments_list:
                s.text = translate_text(
                    s.text.strip(),
                    target_lang='es'
                )
            
            vtt_path = os.path.join(
                settings.MEDIA_ROOT,
                'captions',
                f"{base_name}.vtt"
            )
            os.makedirs(os.path.dirname(vtt_path), exist_ok=True)
            write_webvtt(segments_list, output_path=vtt_path)

            if os.path.exists(vtt_path) and os.path.getsize(vtt_path) > 0:
                instance.vtt_file = os.path.relpath(
                    vtt_path,
                    settings.MEDIA_ROOT
                )
            instance.audio = os.path.relpath(
                audio_path,
                settings.MEDIA_ROOT
            )

        if not instance.thumbnail:
            thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f"{base_name}.jpg")
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            frame_time = clip.duration / 2 if clip.duration <= 4 else 2
            clip.save_frame(thumb_path, t=frame_time)
            instance.thumbnail = os.path.relpath(thumb_path, settings.MEDIA_ROOT)

        clip.close()
        instance.save()

        print("*" * 20)
        print(f"Processed video {video_id} successfully.")

        # Notify the client that the video and vtt file are ready
        expo_token = instance.user.push_notification_token
        message = {
            "to": expo_token,
            "sound": "default",
            "title": "Video Ready!",
            "body": "You have a new task video with captions!",
            "data": {
                "action": "video_ready",
                "video_id": instance.id,
                "video_url": instance.video.url,
                "vtt_url": instance.vtt_file.url
            },
            "priority": "high",
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
        }

        response = requests.post(EXPO_PUSH_ENDPOINT, json=message, headers=headers)
        print(f"Expo push notification response: {response.status_code} - {response.text}")
        response.raise_for_status()

    except Exception as e:
        print(f"Error in Celery task: {e}")
