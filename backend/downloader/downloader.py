import os
import platform
import tempfile
import urllib.request
import zipfile
import tarfile
import stat
from urllib.parse import urlparse
from typing import Callable, Optional, Dict
from backend.downloader.manifest import System, Tool, BINARIES
from backend.config import get_config_path

def get_os() -> System:
    """
    Returns the current operating system represented as a System enum.
    Raises ValueError if the operating system is not supported.
    """
    system = platform.system()
    if system == "Windows":
        return System.WINDOWS
    elif system == "Linux":
        return System.LINUX
    elif system == "Darwin":
        return System.MACOS
    else:
        raise ValueError(f"Unsupported operating system: {system}")

def download_tool(tool: Tool, progress_callback: Optional[Callable[[float], None]] = None) -> str:
    """
    Downloads the specified tool for the current OS into a temporary directory.
    It invokes progress_callback with the download percentage (0.0 to 100.0) as it progresses.
    It returns the absolute path of the downloaded file.
    """
    sys = get_os()
    
    if sys not in BINARIES:
        raise ValueError(f"No binaries defined for system {sys}")
        
    tool_map = BINARIES[sys]
    if tool not in tool_map:
        raise ValueError(f"No download link defined for the requested tool {tool}")
        
    url_str = tool_map[tool]
    
    parsed_url = urlparse(url_str)
    filename = os.path.basename(parsed_url.path)
    if not filename or filename in (".", "/"):
        filename = "downloaded_file"
        
    temp_dir = tempfile.mkdtemp(prefix="morpho-downloader-")
    dest_path = os.path.join(temp_dir, filename)
    
    req = urllib.request.Request(url_str, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
        if response.status != 200:
            raise ValueError(f"Bad status code from {url_str}: {response.status} {response.reason}")
            
        content_length_header = response.headers.get('Content-Length')
        content_length = int(content_length_header) if content_length_header else 0
        
        total_read = 0
        chunk_size = 64 * 1024  # 64KB chunk size
        
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            total_read += len(chunk)
            
            if content_length > 0 and progress_callback is not None:
                percent = (total_read / content_length) * 100.0
                progress_callback(percent)
                
    return dest_path

def get_bin_dir() -> str:
    """
    Creates and returns the absolute path to the 'bin' directory,
    which is located in the same directory as the configuration file.
    """
    config_dir = os.path.dirname(get_config_path())
    bin_dir = os.path.join(config_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    return bin_dir

def extract_executables(archive_path: str) -> Dict[Tool, str]:
    """
    Extracts only the required executables (ffmpeg, cwebp, dwebp, pandoc) 
    from the given archive (zip or tar) into the 'bin' directory.
    Returns a dictionary mapping the binary base name to its absolute path.
    """
    bin_dir = get_bin_dir()
    extracted_paths: Dict[Tool, str] = {}
    target_binaries: Dict[Tool, set[str]] = {
        Tool.FFMPEG: {'ffmpeg', 'ffmpeg.exe'}, Tool.WEBP: {'cwebp', 'cwebp.exe', 'dwebp', 'dwebp.exe'}, Tool.PANDOC: {'pandoc', 'pandoc.exe'}}
    
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, 'r') as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                filename = os.path.basename(info.filename)
                found_tool = next((tool for tool, bins in target_binaries.items() if filename in bins), None)
                if found_tool: 
                    target_path = os.path.join(bin_dir, filename)
                    with z.open(info) as source, open(target_path, "wb") as target:
                        target.write(source.read())
                    
                    # Make it executable (for Unix-like systems)
                    os.chmod(target_path, os.stat(target_path).st_mode | stat.S_IEXEC)
                    
                    extracted_paths[found_tool] = target_path
                    
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path, 'r:*') as t:
            for member in t.getmembers():
                if not member.isfile():
                    continue
                filename = os.path.basename(member.name)
                found_tool = next((tool for tool, bins in target_binaries.items() if filename in bins), None)
                if found_tool:
                    target_path = os.path.join(bin_dir, filename)
                    with t.extractfile(member) as source, open(target_path, "wb") as target:
                        if source:
                            target.write(source.read())
                            
                    # Make it executable (for Unix-like systems)
                    os.chmod(target_path, os.stat(target_path).st_mode | stat.S_IEXEC)
                    
                    extracted_paths[found_tool] = target_path
                    
    return extracted_paths
