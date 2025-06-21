import os
from faster_whisper import WhisperModel


def transcribe_audio(audio_path):
    """
    Transcribe audio using the Whisper model.
    Args:
        audio_path (str): Path to the audio file.
    Returns:
        tuple: Transcription text, list of segments, and info about the transcription.
    """
    model = WhisperModel("small", device="cpu")
    segments_generator, info = model.transcribe(audio_path, beam_size=5)
    
    # Convert generator to list to avoid consuming it
    segments_list = []
    texts = []
    
    for segment in segments_generator:
        segment.text = segment.text.strip()
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        segments_list.append(segment)
        texts.append(segment.text)

    transcription = " ".join(texts)
    return transcription, segments_list, info


def format_timestamp(seconds):
    """
    Format a timestamp in seconds to HH:MM:SS format.
    Args:
        seconds (float): Time in seconds.
    Returns:
        str: Formatted timestamp as HH:MM:SS.mmm.
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"


def write_webvtt(segments, output_path="captions.vtt"):
    """
    Write segments to a WebVTT file.
    Args:
        segments (list): List of segments with start, end, and text attributes.
        output_path (str): Path to the output WebVTT file.
    Returns:
        None
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convert generator to list if it's not already a list
    segments_list = list(segments)
    
    # Validate that we have segments to write
    if not segments_list:
        print(f"Warning: No segments to write to {output_path}")
        # Write a minimal valid WebVTT file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            f.write("00:00:00.000 --> 00:00:01.000\n")
            f.write("No transcription available\n\n")
        return
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            print(f"Writing WebVTT to {output_path} with {len(segments_list)} segments")
            f.write("WEBVTT\n\n")
            
            for i, segment in enumerate(segments_list, 1):
                # Validate segment has required attributes
                if not hasattr(segment, 'start') or not hasattr(segment, 'end') or not hasattr(segment, 'text'):
                    print(f"Warning: Segment {i} missing required attributes")
                    continue
                
                # Format timestamps
                start = format_timestamp(segment.start)
                end = format_timestamp(segment.end)
                
                # Format and write the cue
                f.write(f"{i}\n")  # Add cue identifier
                f.write(f"{start} --> {end}\n")
                f.write(f"{segment.text.strip()}\n\n")
                
            print(f"Successfully wrote {len(segments_list)} segments to {output_path}")
    except Exception as e:
        print(f"Error writing WebVTT file: {e}")
        # Create a minimal valid file in case of error
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("WEBVTT\n\n")
                f.write("00:00:00.000 --> 00:00:01.000\n")
                f.write("Error creating transcription\n\n")
        except Exception as e2:
            print(f"Failed to create fallback WebVTT file: {e2}")