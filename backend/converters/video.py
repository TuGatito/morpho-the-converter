import os
import subprocess
from enum import Enum
from pathlib import Path
from typing import List

class VideoFormat(str, Enum):
    # Video formats
    MP4 = "mp4"
    MKV = "mkv"
    AVI = "avi"
    MOV = "mov"
    WEBM = "webm"
    
    # Audio formats
    MP3 = "mp3"
    WAV = "wav"
    AAC = "aac"
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"

def convert_video(
    ffmpeg_path: str,
    base_video_path: str,
    save_path: str,
    target_format: VideoFormat,
    video_name: str | None = None
) -> str:
    """
    Converts a video file to another format (video or audio) using ffmpeg.
    
    Args:
        ffmpeg_path: Path to the ffmpeg executable.
        base_video_path: Path of the original video.
        save_path: Directory where the converted file will be saved.
        target_format: Format to convert to (use the VideoFormat enum).
        video_name: Optional name for the converted file (without extension). 
                    If not provided, the original file's name will be used.
                    
    Returns:
        The absolute path of the converted file.
    """
    
    # Ensure the destination directory exists
    os.makedirs(save_path, exist_ok=True)
    
    original_path = Path(base_video_path)
    
    # Determine the output filename
    if video_name:
        new_filename = f"{video_name}.{target_format.value}"
    else:
        new_filename = f"{original_path.stem}.{target_format.value}"
        
    output_path = os.path.join(save_path, new_filename)
    
    # Build the ffmpeg command
    command = [
        ffmpeg_path,
        "-y", # Overwrite if the file already exists
        "-i", base_video_path,
        output_path
    ]
    
    # Execute the command
    subprocess.run(command, check=True)
    
    return output_path


def get_supported_formats() -> List[str]:
    """
    Returns a list of strings representing the formats supported for video conversion.
    
    Returns:
        List[str]: A list of supported format extensions.
    """
    return [fmt.value for fmt in VideoFormat]
