import subprocess
from enum import Enum
from typing import Optional, List
from pathlib import Path
from PIL import Image


class ImageFormat(str, Enum):
    """
    Supported image formats for conversion.
    """
    JPEG = "jpeg"
    JPG = "jpg"
    PNG = "png"
    WEBP = "webp"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"


def convert_image(
    webp_bin_path: str,
    original_image_path: str,
    output_dir: str,
    target_format: ImageFormat,
    new_name: Optional[str] = None
) -> str:
    """
    Converts an image to the specified format using either Pillow or the webp binary.

    Args:
        webp_bin_path (str): The file path to the webp binary (e.g., 'cwebp').
        original_image_path (str): The file path to the original image to be converted.
        output_dir (str): The directory where the converted image will be saved.
        target_format (ImageFormat): The desired output format.
        new_name (Optional[str], optional): Optional new name for the output file (without extension).
            If not provided, the original filename will be used.

    Returns:
        str: The absolute path to the newly converted image file.
        
    Raises:
        FileNotFoundError: If the original image does not exist.
        RuntimeError: If the conversion (Pillow or subprocess) fails.
    """
    original_path = Path(original_image_path)
    
    if not original_path.is_file():
        raise FileNotFoundError(f"The original image was not found: {original_image_path}")
        
    # Determine the output filename
    base_name = new_name if new_name else original_path.stem
    extension = target_format.value
    
    output_file_path = Path(output_dir) / f"{base_name}.{extension}"
    
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    if target_format == ImageFormat.WEBP:
        # Use the webp binary (e.g., cwebp) to convert to WEBP
        # Example command: cwebp input.jpg -o output.webp
        try:
            subprocess.run(
                [webp_bin_path, str(original_path), "-o", str(output_file_path)],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"WebP binary conversion failed: {e.stderr}") from e
    else:
        # Use Pillow for all other formats
        try:
            with Image.open(original_path) as img:
                # Convert to RGB if saving as JPEG to avoid transparency issues
                if target_format in (ImageFormat.JPEG, ImageFormat.JPG) and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    
                # Save using the format name (e.g., "JPEG", "PNG")
                img.save(str(output_file_path), format=target_format.name)
        except Exception as e:
            raise RuntimeError(f"Pillow conversion failed: {e}") from e
            
    return str(output_file_path)


def get_supported_formats() -> List[str]:
    """
    Returns a list of strings representing the formats supported for image conversion.
    
    Returns:
        List[str]: A list of supported format extensions.
    """
    return [fmt.value for fmt in ImageFormat]
