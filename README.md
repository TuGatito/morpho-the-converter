# 🐛 Morpho The Converter

**Offline, privacy-first, developer-friendly file converter with a retro TUI and a helpful mascot.**

> Convert images, audio, video, documents, and fonts locally — without ever touching the cloud. Built for game developers, content creators, and terminal lovers.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## 🎯 What is Morpho The Converter?

Morpho is a **desktop application** that performs file conversions entirely on your machine. No uploads, no internet required. It combines a **terminal‑style user interface (TUI)** with the power of industrial‑grade CLI tools (ImageMagick, FFmpeg, Pandoc, FontForge) orchestrated by a lightweight Python backend.

Its unique feature is **Morpho**, a minimalist mascot that guides you through the conversion process: suggesting formats, explaining errors, helping with batch operations, and even giving game‑dev specific advice (sprite sheets, audio looping, texture optimisation).

Ideal for:

- **Game developers** (Godot, Unity, Unreal) who need to crunch assets.
- **Content creators** preparing assets for web or social media.
- **Privacy‑aware users** who never want files to leave their computer.

---

## ✨ Planned Features

| Category | Supported Formats (input → output) |
|----------|-------------------------------------|
| 🖼️ Images | PNG, JPG, WebP, TGA, DDS, BMP, ICO → WebP, JPG, DDS, TGA, PNG |
| 🔊 Audio | WAV, MP3, OGG, FLAC, M4A → OGG, MP3, FLAC, WAV |
| 🎬 Video | MP4, MKV, WEBM, MOV, AVI → MP4, WEBM, MKV |
| 📄 Documents | MD, PDF, HTML, TXT, JSON, YAML → PDF, HTML, TXT (via Pandoc) |
| 🔤 Fonts | TTF, OTF, WOFF, WOFF2 → TTF, OTF, WOFF2 |

**Game‑dev specials:**

- Sprite sheet / texture atlas generation
- Audio looping metadata (OGG `LOOPSTART`/`LOOPLENGTH`)
- Texture optimisation (WebP lossy, oxipng)
- Batch renaming & cleaning

---

## 🧩 Architecture

Morpho uses **PyWebView** (system WebView) to render a HTML/CSS/JS frontend with Alpine.js. The backend is Python, which calls external binaries placed in the `bin/` folder. This keeps the main executable tiny (~10‑15 MB) and leverages mature conversion tools.

MorphoTheConverter/
├── main.py                 # Python entry point, exposes API to JS
├── frontend/               # HTML, CSS, JS, locales
├── backend/                # converter.py, file handling logic
├── bin/                    # external binaries (ImageMagick, ffmpeg, …)
│   ├── windows/
│   ├── linux/
│   └── macos/
└── [roadmap, readme, …]

---

## 🚀 Current Status

We are actively developing Morpho. See the **[Development Roadmap](./ruta_desarrollo.md)** for a detailed checklist of completed and pending phases.

**Completed (Phases 0, 1, 2):**

- Project skeleton, PyWebView window, TUI layout with mascot.
- Drag & drop simulation, theme switching (Matrix, Amber, Dracula, Light).
- Alpine.js reactive state (files, logs, mascot messages).

**Next steps:**

- Dynamic mascot behaviour (Phase 2.5)
- Python ↔ JavaScript bridge (Phase 3)
- Native file/directory dialogs (Phase 4)
- Configuration persistence (Phase 5)
- Actual file conversion using external binaries (Phase 7)

---

## 🧪 How to Run (Development)

### Prerequisites

- Python 3.8 or higher
- [pip](https://pip.pypa.io/) and [venv](https://docs.python.org/3/library/venv.html)
- Git (optional)

### Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/MorphoTheConverter.git
cd MorphoTheConverter

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# Install dependencies
pip install pywebview pyinstaller

# Run the app
python main.py
```

> **Note:** External binaries (ImageMagick, ffmpeg, etc.) are not yet included. The app will work in simulation mode. To enable real conversion, download the tools and place them in the appropriate `bin/<platform>/` folder.

---

## 🛠️ Building Distributables

Use PyInstaller to create standalone executables:

```bash
pyinstaller --onefile --windowed --add-data "frontend:frontend" --add-data "bin:bin" main.py
```

For platform‑specific packaging (`.zip`, `.tar.gz`, `.app`), see the [roadmap](./ruta_desarrollo.md) (Phase 11).

---

## 🤝 Contributing

Morpho is a solo project for now, but feedback and ideas are welcome! Open an issue or reach out.

Areas you could help with:

- Adding more locale translations (Japanese, German, etc.)
- Testing on different Linux distributions or macOS versions
- Suggesting new conversion presets for game engines

---

## 📜 License

MIT — you are free to use, modify, and distribute Morpho, as long as you keep the license notice. The external binaries (ImageMagick, FFmpeg, etc.) have their own licenses (see their respective documentation).

---

## 🧙‍♂️ The Mascot

Morpho (the little `◤M◥`) is your guide. It changes expression and gives contextual advice:

- `◤◡◥` – happy, ready to help
- `◤-◥` – thinking, analysing files
- `◤>◥` – surprised or excited
- `◤x◥` – sad, error or missing tool

Listen to Morpho – it will save you from converting to the wrong format!

---

**Made with 🖤 for the indie game dev community.**  
*Your files never leave your computer – because privacy is not a feature, it's a right.*
