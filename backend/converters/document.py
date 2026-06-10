import subprocess
from enum import Enum
from typing import Optional, List
from pathlib import Path


class DocumentFormat(Enum):
    """
    Commonly supported document formats for conversion via Pandoc.
    """
    MARKDOWN = "md"
    HTML = "html"
    DOCX = "docx"
    ODT = "odt"
    EPUB = "epub"
    PDF = "pdf"
    LATEX = "tex"
    RST = "rst"
    ASCIIDOC = "adoc"
    JSON = "json"


def convert_document(
    pandoc_bin_path: str,
    original_doc_path: str,
    output_dir: str,
    target_format: DocumentFormat,
    new_name: Optional[str] = None
) -> str:
    """
    Converts a document to the specified format using the Pandoc binary.

    Args:
        pandoc_bin_path (str): The file path to the Pandoc binary (e.g., 'pandoc').
        original_doc_path (str): The file path to the original document to be converted.
        output_dir (str): The directory where the converted document will be saved.
        target_format (DocumentFormat): The desired output format.
        new_name (Optional[str], optional): Optional new name for the output file (without extension).
            If not provided, the original filename will be used.

    Returns:
        str: The absolute path to the newly converted document file.
        
    Raises:
        FileNotFoundError: If the original document does not exist.
        RuntimeError: If the Pandoc conversion process fails.
    """
    original_path = Path(original_doc_path)
    
    if not original_path.is_file():
        raise FileNotFoundError(f"The original document was not found: {original_doc_path}")
        
    # Determine the output filename
    base_name = new_name if new_name else original_path.stem
    extension = target_format.value
    
    output_file_path = Path(output_dir) / f"{base_name}.{extension}"
    
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Call Pandoc via subprocess
    # Example command: pandoc input.docx -o output.md
    try:
        subprocess.run(
            [pandoc_bin_path, str(original_path), "-o", str(output_file_path)],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Pandoc conversion failed: {e.stderr}") from e
        
    return str(output_file_path)


def get_supported_formats() -> List[str]:
    """
    Returns a list of strings representing the formats supported by Pandoc
    (based on the DocumentFormat enum).
    
    Returns:
        List[str]: A list of supported format extensions (e.g., 'md', 'html', 'docx').
    """
    return [fmt.value for fmt in DocumentFormat]
