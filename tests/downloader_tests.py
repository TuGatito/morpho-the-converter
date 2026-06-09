import os
import sys

# Agrega la raíz del proyecto al PYTHONPATH para que pueda encontrar el módulo 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import shutil
from backend.downloader.downloader import download_tool, extract_executables, get_bin_dir
from backend.downloader.manifest import Tool

class TestDownloader(unittest.TestCase):
    
    def _test_tool_lifecycle(self, tool: Tool):
        print(f"\n[TEST] Testing lifecycle for tool: {tool.name}")
        
        last_printed = -10
        def progress(percent):
            nonlocal last_printed
            if percent - last_printed >= 25:
                print(f"Downloading {tool.name}: {percent:.1f}%")
                last_printed = percent

        # 1. Download
        try:
            archive_path = download_tool(tool, progress_callback=progress)
        except Exception as e:
            self.fail(f"Failed to download {tool.name}: {e}")
            
        self.assertTrue(os.path.exists(archive_path), f"Archive not found: {archive_path}")
        
        print(f"[TEST] Extracting {tool.name} from {archive_path}...")
        
        # 2. Extract
        try:
            extracted = extract_executables(archive_path)
        except Exception as e:
            self.fail(f"Failed to extract {tool.name}: {e}")
            
        self.assertIn(tool, extracted, f"{tool.name} was not extracted correctly. Found keys: {list(extracted.keys())}")
        
        bin_path = extracted[tool]
        
        # 3. Verify
        self.assertTrue(os.path.exists(bin_path), f"Binary not found: {bin_path}")
        self.assertTrue(os.path.isfile(bin_path), f"Path is not a file: {bin_path}")
        
        # On Windows, os.X_OK might not be as strictly enforced, but it doesn't hurt.
        self.assertTrue(os.access(bin_path, os.X_OK), f"Binary is not executable: {bin_path}")
        
        bin_dir = get_bin_dir()
        self.assertTrue(bin_path.startswith(bin_dir), f"Binary {bin_path} is not in the expected bin dir {bin_dir}")
        
        print(f"[TEST] Successfully downloaded and extracted {tool.name} to: {bin_path}")
        
        # 4. Cleanup
        if os.path.exists(archive_path):
            os.remove(archive_path)

    def test_download_and_extract_pandoc(self):
        """Test downloading and extracting the Pandoc tool."""
        self._test_tool_lifecycle(Tool.PANDOC)

    def test_download_and_extract_webp(self):
        """Test downloading and extracting the WebP tools."""
        self._test_tool_lifecycle(Tool.WEBP)

    def test_download_and_extract_ffmpeg(self):
        """Test downloading and extracting the FFmpeg tool. 
        Note: This might take longer due to the file size."""
        self._test_tool_lifecycle(Tool.FFMPEG)

if __name__ == '__main__':
    unittest.main()
