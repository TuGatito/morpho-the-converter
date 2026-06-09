"""
Manifest definitions for downloading the required conversion tools.
This file maps each tool and operating system to the direct download link 
for its respective static binary or portable release.
"""

from enum import Enum

class System(Enum):
    """
    Enum representing the supported operating systems.
    """
    WINDOWS = 0
    LINUX = 1
    MACOS = 2

class Tool(Enum):
    """
    Enum representing the external command-line tools required by the application.
    """
    FFMPEG = 0  # Used for audio and video conversion
    WEBP = 1    # Used for image processing (contains cwebp, dwebp, etc.)
    PANDOC = 2  # Used for document conversions

# Dictionary mapping operating systems to their specific tool download links.
# These links point to pre-compiled binaries to avoid compilation requirements on the user's machine.
BINARIES = {
    System.WINDOWS: {
        Tool.FFMPEG: "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip",
        Tool.WEBP: "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.6.0-windows-x64.zip",
        Tool.PANDOC: "https://github.com/jgm/pandoc/releases/download/3.10/pandoc-3.10-windows-x86_64.zip",
    },
    System.LINUX: {
        Tool.FFMPEG: "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-lgpl.tar.xz",
        Tool.WEBP: "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.6.0-rc1-linux-x86-64.tar.gz",
        Tool.PANDOC: "https://github.com/jgm/pandoc/releases/download/3.10/pandoc-3.10-linux-amd64.tar.gz",
    },
    System.MACOS: {
        Tool.FFMPEG: "https://evermeet.cx/ffmpeg/ffmpeg-8.1.1.zip",
        Tool.WEBP: "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.6.0-rc1-mac-x86-64.tar.gz",
        Tool.PANDOC: "https://github.com/jgm/pandoc/releases/download/3.10/pandoc-3.10-x86_64-macOS.zip",
    }
}
