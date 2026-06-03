# 📋 Ruta de Desarrollo: MorphoTheConverter (Python + PyWebView)

## 🟢 Fase 0 – Preparación del entorno Python

- [x] 0.1 Crear directorio `MorphoTheConverter/`
- [x] 0.2 Crear subdirectorios: `frontend/` (con `css/`, `js/`, `locales/`), `bin/` (con `windows/`, `linux/`, `macos/`), `backend/`
- [x] 0.3 Crear archivo `main.py` en la raíz
- [x] 0.4 Crear entorno virtual: `python -m venv venv`
- [x] 0.5 Activar entorno virtual e instalar `pywebview` y `pyinstaller`
- [x] 0.6 Verificar que PyWebView funciona con un ejemplo mínimo (ventana vacía)

## 🟢 Fase 1 – Ventana básica y carga del frontend

- [x] 1.1 En `main.py`: importar `webview` y crear una ventana con `webview.create_window()`
- [x] 1.2 Apuntar a `frontend/index.html` (usar `file://` o servir desde `webview` con argumento `url`)
- [x] 1.3 Ejecutar `python main.py` y ver la ventana con el HTML cargado
- [x] 1.4 Ajustar título, tamaño mínimo, posición y capacidad de redimensionar
- [x] 1.5 Asegurar que el cierre de la ventana finaliza el proceso Python correctamente

## 🟢 Fase 2 – Interfaz TUI (HTML/CSS/JS) basada en los bocetos

- [x] 2.1 Crear `frontend/index.html` con estructura de dos columnas (25% / 75%) usando CSS Grid o Flexbox
- [x] 2.2 En la columna izquierda: colocar la mascota (glifo `◤M◥`) dentro de un recuadro, y debajo una burbuja de texto (div con borde y fondo)
- [x] 2.3 En la columna derecha: crear área de arrastre (dropzone), lista de archivos cargados, selectores de formato de salida, selector de carpeta de exportación y botón de conversión
- [x] 2.4 En la parte inferior: panel de logs con desplazamiento vertical y estilo de terminal
- [x] 2.5 En la cabecera: título, versión, selector de idioma (`EN ▼`) y selector de tema (`Matrix ▼`)
- [x] 2.6 Aplicar tipografía monoespaciada (Fira Code, JetBrains Mono, etc.) y bordes con caracteres ASCII simulados (borde sólido, líneas dobles, esquinas redondeadas)
- [x] 2.7 Crear `frontend/css/style.css` con variables CSS para temas (Matrix verde, Ámbar, Dracula, Claro)
- [x] 2.8 Integrar Alpine.js (CDN) y crear el objeto `app()` básico en `frontend/js/app.js` con estado reactivo: `files`, `exportDir`, `logs`, `mascotaTexto`, `mascotaExpresion`, `formatosDisponibles`, etc.
- [x] 2.9 Implementar la simulación visual de drag & drop (resaltado al arrastrar) y mostrar archivos de ejemplo estáticos
- [x] 2.10 Verificar que todos los recursos CSS/JS se cargan correctamente en el WebView

## 🟢 Fase 2.5 – Comportamiento dinámico de la mascota (Morpho)

- [ ] 2.5.1 Definir en Alpine.js un conjunto de mensajes predefinidos para cada situación: inicio, archivo único, múltiples archivos, carpeta, error de binario, conversión exitosa, error de conversión
- [ ] 2.5.2 Asociar cada situación a una expresión (glifo): feliz `◤◡◥`, pensativo `◤-◥`, sorprendido `◤>◥`, triste `◤x◥`
- [ ] 2.5.3 Crear método `actualizarMascota(tipo, datos)` que cambie el texto y la expresión según el contexto
- [ ] 2.5.4 Implementar actualización automática al cargar archivos (cuando cambia `files`)
- [ ] 2.5.5 Asegurar que la mascota recomiende formatos según el tipo de archivo (imagen → WebP/DDS, audio → OGG, video → WEBM)
- [ ] 2.5.6 Hacer que la mascota reaccione a la selección de carpeta de exportación y a los cambios de formato
- [ ] 2.5.7 Probar diferentes escenarios manualmente (sin Python aún) usando datos falsos en Alpine.js

## 🟢 Fase 3 – Puente Python ↔ JavaScript (con soporte para la mascota)

- [ ] 3.1 En `main.py`: exponer una clase Python con `@webview.expose`
- [ ] 3.2 Crear método `log(message)` para imprimir en consola y también enviar al frontend mediante `evaluate_js`
- [ ] 3.3 Desde JS, llamar `pywebview.api.log('mensaje')` y verlo en la terminal
- [ ] 3.4 Crear método `notify_mascota(evento, datos)` que desde Python pueda actualizar el diálogo de la mascota en el frontend (útil para errores de binarios, conversión completada, etc.)
- [ ] 3.5 Probar comunicación bidireccional: JS → Python → JS (actualizando la mascota)

## 🟢 Fase 4 – Selección de archivos y carpetas (diálogos nativos) + integración con mascota

- [ ] 4.1 Exponer método `open_file_dialog()` usando `webview.windows[0].create_file_dialog()`
- [ ] 4.2 Exponer método `open_folder_dialog()` usando `webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)`
- [ ] 4.3 Desde JS, llamar a estos métodos y recibir rutas; actualizar `files` y `exportDir` en Alpine
- [ ] 4.4 Al recibir archivos, llamar a `actualizarMascota` con el tipo correspondiente (un archivo, múltiples, carpeta)
- [ ] 4.5 Si se selecciona una carpeta, pedir confirmación a la mascota ("¿Escanear subcarpetas?") y enviar la respuesta a Python para escanear recursivamente
- [ ] 4.6 Almacenar rutas en el estado y mostrar lista de archivos en la columna derecha

## 🟢 Fase 5 – Persistencia de configuración (idioma, tema, ruta de exportación)

- [ ] 5.1 Usar `configparser` o `json` para guardar en `~/.config/morpho/config.json` (o `AppData`)
- [ ] 5.2 Guardar: `locale`, `theme`, `default_export_path`, `overwrite_policy`
- [ ] 5.3 Al iniciar, cargar configuración y enviarla al frontend mediante `evaluate_js`
- [ ] 5.4 Exponer métodos `set_config(key, value)` y `get_config(key)`
- [ ] 5.5 Al cambiar idioma o tema en la UI, persistir y aplicar cambios (recargar traducciones o CSS)

## 🟢 Fase 6 – Internacionalización (i18n) incluyendo textos de la mascota

- [ ] 6.1 Crear `frontend/locales/en.json`, `es.json` con claves para toda la interfaz y para los mensajes de la mascota
- [ ] 6.2 Crear función Python que cargue el JSON correspondiente al `locale` actual
- [ ] 6.3 Inyectar el objeto de traducciones a `window.translations` y también a Alpine.js (`$store.translations`)
- [ ] 6.4 Modificar la mascota para que use `$store.translations.mascota_mensajes[contexto]`
- [ ] 6.5 Al cambiar de idioma, volver a cargar el JSON y actualizar los textos dinámicamente (sin recargar la página)

## 🟢 Fase 7 – Invocación de binarios externos (conversión simple) y notificaciones a la mascota

- [ ] 7.1 Crear módulo `backend/converter.py` con funciones para ejecutar comandos usando `subprocess`
- [ ] 7.2 Detectar SO (`platform.system()`) para elegir subcarpeta en `bin/`
- [ ] 7.3 Implementar `convert_file(input_path, output_format, category, log_callback)`
- [ ] 7.4 Usar `subprocess.Popen` para ejecutar `magick` (imagen), `ffmpeg` (audio/video), etc.
- [ ] 7.5 Capturar stdout/stderr línea a línea y enviar al callback
- [ ] 7.6 Verificar existencia del binario antes de ejecutar; si falta, llamar a `notify_mascota('bin_faltante', binario)` desde Python para que la mascota muestre un mensaje de ayuda
- [ ] 7.7 Probar conversión básica (PNG → WebP) desde la UI, mostrando logs y actualizando la mascota al terminar (éxito o error)

## 🟢 Fase 8 – Conversión por lotes y feedback en tiempo real (con progreso)

- [ ] 8.1 Modificar `converter.py` para procesar lista de archivos en un hilo separado (usando `threading`)
- [ ] 8.2 Calcular ruta de salida: respetar `exportDir` o usar `origen/_converted`
- [ ] 8.3 Enviar progreso al frontend (archivo actual, índice, total) mediante `evaluate_js`
- [ ] 8.4 Mostrar barra de progreso en la columna derecha (opcional) y actualizar logs
- [ ] 8.5 Añadir opción de sobrescribir o renombrar (configurable)
- [ ] 8.6 Permitir cancelar el proceso con `threading.Event`; la mascota debe confirmar la cancelación

## 🟢 Fase 9 – Detección automática de categoría y recomendaciones de la mascota

- [ ] 9.1 Definir en Python diccionario `ext -> categoria` (imagen, audio, video, documento, fuente)
- [ ] 9.2 Al recibir archivos, clasificarlos y enviar resumen al frontend (ej. "5 imágenes, 2 audios")
- [ ] 9.3 La mascota debe sugerir formatos por defecto según la categoría mayoritaria o según cada grupo
- [ ] 9.4 Generar dinámicamente en el HTML los selectores de formato para cada categoría presente (usando `x-for`)
- [ ] 9.5 Al iniciar conversión, pasar la categoría correcta a `convert_file`

## 🟢 Fase 10 – Funcionalidades para Game Dev (adicionales)

- [ ] 10.1 **Generador de Sprite Sheet**: botón que ejecute `montage` de ImageMagick sobre una secuencia de frames (detectados por nombre numerado)
- [ ] 10.2 **Audio Looping**: en la UI, si se convierte a OGG, mostrar checkboxes para definir `loopstart` y `looplength`; usar ffmpeg para inyectar metadatos
- [ ] 10.3 **Optimización de texturas**: perfil que ejecute `oxipng` (sin pérdida) o `webp` con calidad configurable (deslizador)
- [ ] 10.4 **Atlas de iconos**: herramienta para juntar imágenes en una sola textura y generar JSON de posiciones (usando ImageMagick)
- [ ] 10.5 **Batch renombrado**: utilidad para limpiar nombres (minúsculas, guiones, eliminar acentos) – se puede hacer con Python puro

## 🟢 Fase 11 – Empaquetado con PyInstaller

- [ ] 11.1 Reunir binarios externos (ImageMagick, FFmpeg, Pandoc, FontForge) en `bin/windows`, `bin/linux`, `bin/macos`
- [ ] 11.2 Crear spec de PyInstaller que incluya `frontend/` y `bin/` como datos adicionales (`--add-data`)
- [ ] 11.3 Ejecutar `pyinstaller --onefile --windowed --add-data "frontend:frontend" --add-data "bin:bin" main.py`
- [ ] 11.4 Probar ejecutable en Windows (máquina virtual o real)
- [ ] 11.5 Probar en Linux (requiere WebKitGTK, se puede incluir en AppImage)
- [ ] 11.6 Probar en macOS (asegurar rutas relativas a `bin`)
- [ ] 11.7 Crear scripts de lanzamiento (`.bat`, `.sh`) para facilitar la ejecución
- [ ] 11.8 Empaquetar en `.zip` (Windows), `.tar.gz` (Linux), `.app` (macOS)

## 🟢 Fase 12 – Pulido final y documentación

- [ ] 12.1 Añadir atajos de teclado (Ctrl+O abrir archivos, Ctrl+E abrir carpeta de exportación, Ctrl+L limpiar logs, Ctrl+Enter convertir)
- [ ] 12.2 Implementar temas adicionales (Dracula, Solarized, Claro/Oscuro) usando CSS Variables y persistencia
- [ ] 12.3 Mostrar mensajes de error amigables cuando falta un binario, con botones de ayuda (abrir carpeta bin, descargar)
- [ ] 12.4 Escribir README.md con instrucciones de instalación, requisitos (Python, PyWebView, binarios externos) y ejemplos de uso
- [ ] 12.5 Grabar video demo (2-3 minutos) mostrando la interfaz, la mascota y las conversiones principales
- [ ] 12.6 Publicar en Itch.io y compartir en comunidades (Reddit, Discord de game devs)
