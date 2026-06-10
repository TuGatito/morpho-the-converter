import os
import subprocess
from enum import Enum
from pathlib import Path
from typing import List

class AudioFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    AAC = "aac"
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"

def convert_audio(
    ffmpeg_path: str,
    base_audio_path: str,
    save_path: str,
    target_format: AudioFormat,
    audio_name: str | None = None
) -> str:
    """
    Converts an audio file to another format using ffmpeg.
    
    Args:
        ffmpeg_path: Path to the ffmpeg executable.
        base_audio_path: Path of the original audio.
        save_path: Directory where the converted audio will be saved.
        target_format: Format to convert to (use the AudioFormat enum).
        audio_name: Optional name for the converted file (without extension). 
                    If not provided, the original file's name will be used.
                    
    Returns:
        The absolute path of the converted file.
    """
    
    # Ensure the destination directory exists
    os.makedirs(save_path, exist_ok=True)
    
    original_path = Path(base_audio_path)
    
    # Determine the output filename
    if audio_name:
        new_filename = f"{audio_name}.{target_format.value}"
    else:
        new_filename = f"{original_path.stem}.{target_format.value}"
        
    output_path = os.path.join(save_path, new_filename)
    
    # Build the ffmpeg command
    command = [
        ffmpeg_path,
        "-y", # Overwrite if the file already exists
        "-i", base_audio_path,
        output_path
    ]
    
    # Execute the command
    subprocess.run(command, check=True)
    
    return output_path


def get_supported_formats() -> List[str]:
    """
    Returns a list of strings representing the formats supported for audio conversion.
    
    Returns:
        List[str]: A list of supported format extensions (e.g., 'mp3', 'wav').
    """
    return [fmt.value for fmt in AudioFormat]
