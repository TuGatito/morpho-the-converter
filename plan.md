## 🎯 Lista de Metas (Checklist para Issues / Pull Requests)

### 🔳 Hito 1: Inicialización y Configuración Base

* [x] Inicializar el proyecto configurando el entorno para `pywebview` (usar Vanilla/Plain HTML ya que usaremos Alpine.js directo).
* [x] Configurar `main.py` para que la ventana sea **frameless** (sin bordes del sistema) y definir el tamaño inicial.
* [x] Crear el módulo `py_backend/config` para leer/escribir un archivo JSON local (guardar idioma y tema).
* [x] **PR #1: Base del proyecto y persistencia de configuración.**

### 🔳 Hito 2: El Motor de Verificación y Descarga Local (Downloader Core)

* [x] **Mapear Manifiesto de Enlaces (`manifest.py`):** Crear un mapa con las URLs directas a las versiones portables/estáticas de FFmpeg, ImageMagick (o webp tools) y Pandoc para Windows, Linux y macOS.
* [x] **Rutina de Escaneo:** Desarrollar en `converter.py` la función que revise el disco duro buscando la presencia de los ejecutables requeridos (`ffmpeg`, `magick`, etc.) con sus respectivas extensiones de sistema.
* [x] **Manejador de Descargas Nativo:** Implementar la lógica con `urllib.request` (o `requests`) para descargar los paquetes comprimidos mostrando el porcentaje de progreso.
* [x] **Extractor de Binarios Sueltos:** Programar las funciones nativas en Python usando `zipfile` y `tarfile` para extraer *únicamente* los ejecutables necesarios hacia la carpeta destino, descartando la basura del zip.
* [x] **Permisos de Ejecución Unix:** Asegurar que tras extraer en Linux/macOS, se ejecute un `os.chmod(path, 0o755)` para otorgar permisos de ejecución al binario de manera automática.
* [x] **PR #2: Sistema autónomo de diagnóstico, descarga y extracción de herramientas.**

### 🔳 Hito 3: La API de Conversión Acoplada (Execution Engine)

* [ ] Modificar las firmas de los métodos en `audio.py`, `video.py`, `image.py`, `document.py` y `font.py` para que consuman dinámicamente el path verificado que entregue el módulo `downloader`.
* [ ] Implementar la ejecución interna mediante `subprocess`, capturando correctamente las salidas de error estándar (*stderr*) para pasárselas al glifo en caso de que una conversión falle internamente.
* [ ] Validar el soporte para colas de procesamiento por lotes (procesar secuencialmente o en paralelo mediante `concurrent.futures` o `threading` el array de archivos arrastrados).
* [ ] **PR #3: API modular de conversión conectada a binarios locales bajo demanda.**

### 🔳 Hito 4: Frontend TUI y Drag & Drop

* [ ] Diseñar el layout HTML/CSS con fuentes *monospaced* simulando una terminal clásica.
* [ ] Crear la barra de título personalizada en HTML y usar las capacidades de arrastre (o la API de drag de pywebview) para poder mover la ventana.
* [ ] Implementar el sistema de *Drag and Drop* nativo de HTML5 en la zona principal y capturar las rutas de los archivos.
* [ ] Diseñar los estados visuales del "Glifo Asistente" (ej. Reposo `( o_o)`, Procesando `( *_-)*`, Éxito `( ^_^)b`).
* [ ] **PR #4: Frontend TUI estático y eventos de arrastre.**

### 🔳 Hito 5: Conexión Final y Pulido

* [ ] Ligar los eventos de *Drag & Drop* de Alpine.js con los métodos del backend expuestos a través de `window.pywebview.api`.
* [ ] Pasar el estado de la conversión al Glifo en tiempo real para que cambie de expresión según el progreso.
* [ ] Probar el empaquetado portable final (por ejemplo, usando `pyinstaller`).
* [ ] **PR #5: Integración total y lanzamiento de la versión Alpha.**