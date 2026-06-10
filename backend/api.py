import os
import platform
import shutil
import threading
from typing import List, Dict, Optional
from enum import Enum
import webview

# Import modular converter functions and formats
from backend.converters.audio import convert_audio, AudioFormat, get_supported_formats as get_audio_formats
from backend.converters.video import convert_video, VideoFormat, get_supported_formats as get_video_formats
from backend.converters.document import convert_document, DocumentFormat, get_supported_formats as get_document_formats
from backend.converters.image import convert_image, ImageFormat, get_supported_formats as get_image_formats
from backend.converters.font import convert_font, FontFormat, get_supported_formats as get_font_formats

# Import configuration helpers
from backend.config import config_exists, read_config, update_config

# Import binary scanner and downloader utilities
from backend.converter import check_system_tools
from backend.downloader.downloader import download_tool, extract_executables, get_bin_dir
from backend.downloader.manifest import Tool


class ConversionCategory(str, Enum):
    """
    Supported conversion categories.
    """
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    IMAGE = "image"
    FONT = "font"


class API:
    """
    Exposed API for pywebview.
    Provides backend operations to the frontend interface.
    """
    def __init__(self):
        self.window = None  # Assigned when creating the window in main.py

    def set_window(self, window):
        """
        Sets the webview window instance to allow sending events.
        
        Args:
            window: The webview window object.
        """
        self.window = window

    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Returns a dictionary containing supported formats for each conversion category.
        
        Returns:
            Dict[str, List[str]]: A dictionary mapping categories to format extensions.
        """
        return {
            ConversionCategory.AUDIO.value: get_audio_formats(),
            ConversionCategory.VIDEO.value: get_video_formats(),
            ConversionCategory.DOCUMENT.value: get_document_formats(),
            ConversionCategory.IMAGE.value: get_image_formats(),
            ConversionCategory.FONT.value: get_font_formats(),
        }

    # --- Configuration Management ---

    def config_exists(self) -> bool:
        """
        Checks if the configuration file exists on the system.
        
        Returns:
            bool: True if it exists, False otherwise.
        """
        return config_exists()

    def read_config(self) -> dict:
        """
        Reads and returns the application configuration as a dictionary.
        
        Returns:
            dict: Dictionary representation of the Config object.
        """
        return read_config().to_dict()

    def update_config(self, lang: str, theme: str) -> None:
        """
        Updates the configuration with new user preferences.
        
        Args:
            lang (str): The language code (e.g., 'es', 'en').
            theme (str): The name of the theme (e.g., 'dracula').
        """
        update_config(lang, theme)

    # --- Binary Diagnosis & Paths ---

    def _get_tool_path(self, name: str) -> Optional[str]:
        """
        Resolves the absolute path to a tool (ffmpeg, cwebp, pandoc),
        checking first the system PATH and then the local bin directory.
        
        Args:
            name (str): The name of the tool ("ffmpeg", "webp", or "pandoc").
            
        Returns:
            Optional[str]: The absolute path to the executable, or None if not found.
        """
        cmd_name = "cwebp" if name == "webp" else name
        
        # Check system PATH
        system_path = shutil.which(cmd_name)
        if system_path:
            return system_path
            
        # Check local config bin directory
        bin_dir = get_bin_dir()
        ext = ".exe" if platform.system() == "Windows" else ""
        local_path = os.path.join(bin_dir, f"{cmd_name}{ext}")
        if os.path.isfile(local_path):
            return local_path
            
        return None

    def check_binaries(self) -> Dict[str, bool]:
        """
        Verifies if required binary dependencies are installed system-wide or locally.
        
        Returns:
            Dict[str, bool]: A mapping of tool name to installation status.
        """
        status = check_system_tools()
        bin_dir = get_bin_dir()
        ext = ".exe" if platform.system() == "Windows" else ""
        
        if not status["ffmpeg"]:
            local_ffmpeg = os.path.join(bin_dir, f"ffmpeg{ext}")
            status["ffmpeg"] = os.path.isfile(local_ffmpeg)
            
        if not status["webp"]:
            local_cwebp = os.path.join(bin_dir, f"cwebp{ext}")
            status["webp"] = os.path.isfile(local_cwebp)
            
        if not status["pandoc"]:
            local_pandoc = os.path.join(bin_dir, f"pandoc{ext}")
            status["pandoc"] = os.path.isfile(local_pandoc)
            
        return status

    def get_binary_paths(self) -> Dict[str, Optional[str]]:
        """
        Retrieves the absolute path to the binary dependencies.
        
        Returns:
            Dict[str, Optional[str]]: A dictionary mapping tool names to paths.
        """
        return {
            "ffmpeg": self._get_tool_path("ffmpeg"),
            "webp": self._get_tool_path("webp"),
            "pandoc": self._get_tool_path("pandoc")
        }

    # --- Binary Downloader ---

    def download_binaries(self) -> dict:
        """
        Asynchronously initiates the download process for any missing binaries.
        
        Returns:
            dict: The download task start response.
        """
        threading.Thread(target=self._run_downloads, daemon=True).start()
        return {"status": "download_started"}

    def _run_downloads(self) -> None:
        """
        Performs sequential downloads and extractions of all missing tools.
        Notifies progress and completion events to the webview frontend.
        """
        status = self.check_binaries()
        tools_to_download = []
        
        if not status["ffmpeg"]:
            tools_to_download.append((Tool.FFMPEG, "ffmpeg"))
        if not status["webp"]:
            tools_to_download.append((Tool.WEBP, "webp"))
        if not status["pandoc"]:
            tools_to_download.append((Tool.PANDOC, "pandoc"))
            
        if not tools_to_download:
            self._notify_frontend("download_complete", {"status": "all_installed"})
            return
            
        total_tools = len(tools_to_download)
        
        for i, (tool, name) in enumerate(tools_to_download, start=1):
            try:
                self._notify_frontend("download_progress", {
                    "tool": name,
                    "index": i,
                    "total": total_tools,
                    "progress": 0.0,
                    "status": "downloading"
                })
                
                # Dynamic closure progress callback
                def progress_cb(percent: float):
                    self._notify_frontend("download_progress", {
                        "tool": name,
                        "index": i,
                        "total": total_tools,
                        "progress": percent,
                        "status": "downloading"
                    })
                
                archive_path = download_tool(tool, progress_callback=progress_cb)
                
                self._notify_frontend("download_progress", {
                    "tool": name,
                    "index": i,
                    "total": total_tools,
                    "progress": 100.0,
                    "status": "extracting"
                })
                
                extract_executables(archive_path)
                
                # Attempt file cleanup of temporary downloaded package
                try:
                    if os.path.exists(archive_path):
                        os.remove(archive_path)
                        # Also clean up the temporary folder directory
                        os.rmdir(os.path.dirname(archive_path))
                except Exception:
                    pass
                    
            except Exception as e:
                self._notify_frontend("download_error", {
                    "tool": name,
                    "error": str(e)
                })
                return
                
        self._notify_frontend("download_complete", {"status": "success"})

    # --- Batch File Conversions ---

    def process_batch(self, file_paths: List[str], save_path: str, target_format: str, category: str) -> dict:
        """
        Starts the batch file conversion queue in a background worker thread
        to keep the PyWebview UI responsive.
        
        Args:
            file_paths (List[str]): List of absolute input file paths.
            save_path (str): Directory where converted files will be saved.
            target_format (str): Desired output format extension.
            category (str): Conversion category string (e.g., 'audio').
            
        Returns:
            dict: The processing queue start response.
        """
        threading.Thread(
            target=self._run_batch_conversion,
            args=(file_paths, save_path, target_format, category),
            daemon=True
        ).start()
        
        return {"status": "processing", "message": "Queue initiated"}

    def _run_batch_conversion(self, file_paths: List[str], save_path: str, target_format: str, category: str) -> None:
        """
        Runs sequentially through the conversion queue list in the background.
        
        Args:
            file_paths (List[str]): List of input file paths.
            save_path (str): Target output directory path.
            target_format (str): Destination file extension.
            category (str): Conversion category string.
        """
        total_files = len(file_paths)
        
        try:
            # Parse the string category into the enum
            cat_enum = ConversionCategory(category)
        except ValueError:
            self._notify_frontend("batch_error", {"error": f"Unsupported category: {category}"})
            return
            
        for index, current_file in enumerate(file_paths, start=1):
            try:
                # Notify frontend about which file is current to animate the glyph
                self._notify_frontend("batch_progress", {
                    "current": index,
                    "total": total_files,
                    "file": current_file,
                    "status": "converting"
                })

                # Route conversion to correct pipeline according to category
                if cat_enum == ConversionCategory.AUDIO:
                    audio_fmt = AudioFormat(target_format)
                    ffmpeg_path = self._get_tool_path("ffmpeg") or "ffmpeg"
                    convert_audio(
                        ffmpeg_path=ffmpeg_path,
                        base_audio_path=current_file,
                        save_path=save_path,
                        target_format=audio_fmt
                    )
                elif cat_enum == ConversionCategory.VIDEO:
                    video_fmt = VideoFormat(target_format)
                    ffmpeg_path = self._get_tool_path("ffmpeg") or "ffmpeg"
                    convert_video(
                        ffmpeg_path=ffmpeg_path,
                        base_video_path=current_file,
                        save_path=save_path,
                        target_format=video_fmt
                    )
                elif cat_enum == ConversionCategory.DOCUMENT:
                    doc_fmt = DocumentFormat(target_format)
                    pandoc_path = self._get_tool_path("pandoc") or "pandoc"
                    convert_document(
                        pandoc_bin_path=pandoc_path,
                        original_doc_path=current_file,
                        output_dir=save_path,
                        target_format=doc_fmt
                    )
                elif cat_enum == ConversionCategory.IMAGE:
                    img_fmt = ImageFormat(target_format)
                    webp_path = self._get_tool_path("webp") or "cwebp"
                    convert_image(
                        webp_bin_path=webp_path,
                        original_image_path=current_file,
                        output_dir=save_path,
                        target_format=img_fmt
                    )
                elif cat_enum == ConversionCategory.FONT:
                    font_fmt = FontFormat(target_format)
                    convert_font(
                        original_font_path=current_file,
                        output_dir=save_path,
                        target_format=font_fmt
                    )

            except Exception as e:
                # Report file conversion failure and keep processing the remaining queue
                self._notify_frontend("batch_file_error", {
                    "file": current_file,
                    "error": str(e)
                })

        # Notify frontend conversion queue finished
        self._notify_frontend("batch_complete", {"total": total_files})

    def _notify_frontend(self, event_name: str, data: dict) -> None:
        """
        Sends reactive dispatch events to webview window executing JS listeners.
        
        Args:
            event_name (str): Custom JavaScript event name.
            data (dict): Data dictionary to be serialized as details.
        """
        if self.window:
            # Dispatches custom events on Alpine.js / general listeners
            self.window.evaluate_js(
                f"window.dispatchEvent(new CustomEvent('{event_name}', {{detail: {data}}}));"
            )