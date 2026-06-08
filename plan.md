## 🎯 Lista de Metas (Checklist para Issues / Pull Requests)

### 🔳 Hito 1: Inicialización y Configuración Base

* [x] Inicializar el proyecto con `wails init` (usar el template *vanilla* o *plain* ya que usaremos Alpine.js directo).
* [x] Configurar `main.go` para que la ventana sea **frameless** (sin bordes del sistema) y definir el tamaño inicial.
* [x] Crear el módulo `backend/config` para leer/escribir un archivo JSON local (guardar idioma y tema).
* [x] **PR #1: Base del proyecto y persistencia de configuración.**

### 🔳 Hito 2: Gestión de Binarios y Comandos Externos

* [ ] Implementar en Go el detector de Sistema Operativo (`runtime.GOOS`).
* [ ] Crear la lógica para ejecutar comandos usando las rutas relativas de `bin/windows/` o `bin/linux/`.
* [ ] Validar que los binarios tengan permisos de ejecución correctos al iniciar la app (especialmente en Linux).
* [ ] **PR #2: Helper de ejecución de binarios multiplataforma.**

### 🔳 Hito 3: API de Conversión (Módulos de Go)

* [ ] Desarrollar `video.go` y `audio.go` (integración inicial con FFmpeg para pruebas).
* [ ] Desarrollar `image.go`, `document.go` y `font.go` (maquetar los métodos aunque usen *mocks* o binarios provisionales).
* [ ] Asegurar que los métodos soporten procesamiento por lotes (arrays de rutas).
* [ ] **PR #3: API completa de conversión en el Backend.**

### 🔳 Hito 4: Frontend TUI y Drag & Drop

* [ ] Diseñar el layout HTML/CSS con fuentes *monospaced* simulando una terminal clásica.
* [ ] Crear la barra de título personalizada en HTML y usar la propiedad de Wails `--wails-drop-target: top` (o el sistema de drag nativo de Wails) para poder mover la ventana.
* [ ] Implementar el sistema de *Drag and Drop* nativo de HTML5 en la zona principal y capturar las rutas de los archivos.
* [ ] Diseñar los estados visuales del "Glifo Asistente" (ej. Reposo `( o_o)`, Procesando `( *_-)*`, Éxito `( ^_^)b`).
* [ ] **PR #4: Frontend TUI estático y eventos de arrastre.**

### 🔳 Hito 5: Conexión Final y Pulido

* [ ] Ligar los eventos de *Drag & Drop* de Alpine.js con los métodos del backend generados en `wailsjs/go/`.
* [ ] Pasar el estado de la conversión al Glifo en tiempo real para que cambie de expresión según el progreso.
* [ ] Probar el empaquetado portable final con `wails build`.
* [ ] **PR #5: Integración total y lanzamiento de la versión Alpha.**