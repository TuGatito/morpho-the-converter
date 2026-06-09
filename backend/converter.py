import shutil

def check_system_tools() -> dict[str, bool]:
    """
    Checks the system PATH for the required executables: ffmpeg, webp (or cwebp), and pandoc.
    It returns a dictionary indicating whether each tool is installed/available.
    """
    tools = ["ffmpeg", "webp", "pandoc"]
    status = {}
    
    for tool in tools:
        status[tool] = shutil.which(tool) is not None
        
    # WebP tools might be installed as "cwebp" instead of a command named "webp"
    if not status.get("webp"):
        status["webp"] = shutil.which("cwebp") is not None
        
    return status
