from celery import shared_task
from .models import VideoRawUpload
from .utils import extract_audio, transcribe_audio, translate_transcription, notify_user

@shared_task
def process_uploaded_video(video_id):
    video = VideoRawUpload.objects.get(id=video_id)
    
    audio_path = extract_audio(video.video.path)
    vtt_file = transcribe_audio(audio_path)
    translated_vtt = translate_transcription(vtt_file, target_lang='hr')
    
    notify_user(video.user.expo_push_token, video.id)
