# Morpho The Converter 🦋

An offline, privacy-first, ultra-lightweight desktop application that acts as a local alternative to online file converters like Convertio. Built with **Go**, **Wails**, and **Alpine.js**, Morpho packs all its dependencies into a single, fully portable executable—no installers, no cloud uploads, and zero configuration required.

The interface breaks away from traditional OS windows, featuring a minimalist **Text User Interface (TUI)** aesthetic driven exclusively by Drag-and-Drop workflows, complete with a reactive ASCII glyph assistant.

---

## ✨ Features

*   **100% Offline & Private:** Your files never leave your machine. All conversions happen locally using embedded binaries.
*   **Zero-Installation Portability:** A single executable binary for your system. Drop it anywhere (like a USB drive) and run it.
*   **Multi-Format Universal API:** Modular backend support for processing:
    *   **Images:** Format swapping, resizing, and compression.
    *   **Audio & Video:** Fast transcodings, extracts, and remuxing via optimized local pipelines.
    *   **Documents:** Local schema and document format transformations.
    *   **Fonts:** Cross-compatible web and desktop font generation.
*   **Batch Processing:** Drag and drop a single file, a cluster of selected assets, or an entire directory to queue up mass conversions.
*   **Immersive TUI Styling:** A distraction-free, terminal-inspired interface with custom headers for borderless dragging, minimizing, and closing.
*   **Reactive Glyph Assistant:** No cluttered, hard-to-read progress logs. A retro ASCII-art character reacts dynamically to guide you through idling, processing, success, or error states.
*   **Persistent Configuration:** Remembers your UI theme and language preferences locally without standard heavy registry entries.

---

## 📂 Project Architecture

The project decouples frontend Presentation from system-level Execution through Wails bindings, keeping cross-platform compilation clean:

```text
morpho-the-converter/
├── bin/                       # Platform-specific native binaries (e.g., FFmpeg, Pandoc)
│   ├── windows/
│   └── linux/
├── backend/                   # Pure Go Core
│   ├── config/                # JSON State & Preference management (Language, Theme)
│   └── converter/             # Native execution pipelines split by MIME-types
│       ├── converter.go       # Core OS-sniffing runner & file orchestrator
│       ├── audio.go           
│       ├── video.go           
│       ├── image.go           
│       ├── document.go        
│       └── font.go            
├── frontend/                  # Lightweight TUI Presentation
│   └── src/
│       ├── index.html         # Borderless framing
│       ├── css/style.css      # Monospaced typography & terminal aesthetics
│       └── js/app.js          # Alpine.js state-machine & Wails API bindings
├── main.go                    # Wails runtime configuration lifecycle
├── app.go                     # Entrypoint exposing Go methods to Frontend context
└── wails.json                 # Native window flags (Frameless, Dimensions, Drop-Targets)