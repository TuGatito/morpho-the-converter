from enum import Enum
from pathlib import Path
from typing import Optional, List

from fontTools.ttLib import TTFont


class FontFormat(str, Enum):
    """
    Supported font formats for conversion.
    """
    TTF = "ttf"
    OTF = "otf"
    WOFF = "woff"
    WOFF2 = "woff2"


def convert_font(
    original_font_path: str,
    output_dir: str,
    target_format: FontFormat,
    new_name: Optional[str] = None
) -> str:
    """
    Converts a font to the specified format using fontTools.
    The brotlicffi library is used implicitly by fontTools for WOFF2 conversion.

    Args:
        original_font_path (str): The file path to the original font to be converted.
        output_dir (str): The directory where the converted font will be saved.
        target_format (FontFormat): The desired output format.
        new_name (Optional[str], optional): Optional new name for the output file (without extension).
            If not provided, the original filename will be used.

    Returns:
        str: The absolute path to the newly converted font file.
        
    Raises:
        FileNotFoundError: If the original font does not exist.
        RuntimeError: If the conversion fails.
    """
    original_path = Path(original_font_path)
    
    if not original_path.is_file():
        raise FileNotFoundError(f"The original font was not found: {original_font_path}")
        
    # Determine the output filename
    base_name = new_name if new_name else original_path.stem
    extension = target_format.value
    
    output_file_path = Path(output_dir) / f"{base_name}.{extension}"
    
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Open the font using fontTools
        font = TTFont(str(original_path))
        
        # Determine the flavor based on the target format
        # TTF and OTF have flavor = None
        # WOFF has flavor = "woff"
        # WOFF2 has flavor = "woff2"
        if target_format in (FontFormat.WOFF, FontFormat.WOFF2):
            font.flavor = target_format.value
        else:
            font.flavor = None
            
        # Save the converted font
        font.save(str(output_file_path))
    except Exception as e:
        raise RuntimeError(f"Font conversion failed: {e}") from e
        
    return str(output_file_path)


def get_supported_formats() -> List[str]:
    """
    Returns a list of strings representing the formats supported for font conversion.
    
    Returns:
        List[str]: A list of supported format extensions (e.g., 'ttf', 'woff2').
    """
    return [fmt.value for fmt in FontFormat]
