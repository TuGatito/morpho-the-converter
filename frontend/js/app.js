function app() {
  return {
    // Estado reactivo
    selectedLanguage: 'es',
    mascotaExpresion: '◤◡◥',
    mascotaTexto: '¡Hola! Soy Morpho. Arrastra cualquier archivo para ver las conversiones disponibles.',
    files: [],          // lista de objetos { name, type, path? }
    exportDir: '',
    selectedFormat: 'webp',
    logs: [],
    dragOver: false,
    nextLogId: 1,

    /**
     * Get localized text for the current language using a dot-separated path.
     * Example: `getText('header.title')` -> "Morpho The Converter v1.0"
     *
     * @param {string} path - Dot-separated key path to the desired text (e.g. "header.title").
     * @returns {string} Localized string if found; otherwise returns the original `path`.
     */
    getText(path) {
      const lang = this.selectedLanguage || 'es';
      // Intentar encontrar el objeto de locales en varios lugares (global, window)
      let allLocales = typeof locales !== 'undefined' ? locales : (typeof window !== 'undefined' ? window.locales : undefined);
      // Si no está disponible, intentar import dinámico relativo a este archivo (fallback no bloqueante)
      if (!allLocales) {
        try {
          // import() devuelve una promesa; aquí hacemos un intento sincrónico devolviendo el path si falla
          // ruta relativa desde `js/app.js` hacia `locales/locales.js`
          import('../locales/locales.js').then(mod => {
            allLocales = mod.locales || mod.default || mod;
            return null;
          }).catch(() => null);
        } catch (err) {
          // Ignorar, seguiremos con undefined
        }
      }

      if (!allLocales) return path;

      const root = allLocales[lang];
      if (!root) return path;

      const parts = String(path).split('.');
      let cur = root;
      for (let i = 0; i < parts.length; i++) {
        const key = parts[i];
        if (cur && typeof cur === 'object' && key in cur) cur = cur[key];
        else return path;
      }
      if (typeof cur === 'string') return cur;
      try { return JSON.stringify(cur); } catch (e) { return path; }
    },

    init() {
      // Log de bienvenida
      this.addLog('Sistema listo. Esperando archivos...');
      this.addLog('Morpho: Puedes arrastrar múltiples archivos o una carpeta entera.');
      // Cargar configuración simulada
      this.exportDir = 'origen/_converted';
    },

    addLog(msg) {
      this.logs.push({ id: this.nextLogId++, text: msg });
      this.$nextTick(() => {
        const container = this.$refs.logsContainer;
        if (container) container.scrollTop = container.scrollHeight;
      });
    },

    handleDrop(event) {
      this.dragOver = false;
      // Simulación: solo mostramos nombres de archivo (sin ruta real aún)
      const items = event.dataTransfer.items;
      const newFiles = [];
      for (let i = 0; i < items.length; i++) {
        const file = items[i].getAsFile();
        if (file) {
          let type = 'desconocido';
          if (file.type.startsWith('image/')) type = 'imagen';
          else if (file.type.startsWith('audio/')) type = 'audio';
          else if (file.type.startsWith('video/')) type = 'video';
          newFiles.push({ name: file.name, type: type, path: '' });
        }
      }
      if (newFiles.length === 0) {
        // Si es carpeta, simulamos
        this.addLog('Simulación: Se detectó una carpeta. Próximamente escaneo real.');
        this.mascotaTexto = 'Has arrastrado una carpeta. Voy a escanear todos los archivos compatibles. ¿Procesamos todo?';
        this.mascotaExpresion = '◤>◥';
      } else {
        this.files = newFiles;
        this.addLog(`${newFiles.length} archivo(s) cargado(s).`);
        if (newFiles.length === 1) {
          const f = newFiles[0];
          this.mascotaTexto = `He detectado un archivo ${f.type}. Puedo convertirlo a varios formatos. ¿Cuál prefieres?`;
          this.mascotaExpresion = '◤-◥';
        } else {
          this.mascotaTexto = 'Hay varios tipos. Puedes convertirlos al mismo formato (si tienen soporte) o elegir por tipo. Te recomiendo WebP para imágenes, OGG para audio.';
          this.mascotaExpresion = '◤◡◥';
        }
      }
    },

    selectOutputDir() {
      // Simulación: luego será llamado a Python
      this.addLog('Abrir diálogo de carpeta (pendiente integración con Python)');
    },

    startConversion() {
      if (this.files.length === 0) return;
      this.addLog(`Iniciando conversión de ${this.files.length} archivo(s) a ${this.selectedFormat}...`);
      this.mascotaTexto = '¡Empezando conversión! Revisa el panel de logs para seguir el progreso.';
      this.mascotaExpresion = '◤◡◥';
      // Simular proceso asíncrono
      setTimeout(() => {
        this.addLog('✅ Conversión completada con éxito.');
        this.mascotaTexto = '¡Listo! Tus archivos están en la carpeta de salida.';
        this.mascotaExpresion = '◤◡◥';
      }, 2000);
    },

    setLanguage(lang) {
      this.addLog(`Cambiando idioma a ${lang.toUpperCase()} (pendiente traducciones)`);
      // Aquí se integrará i18n más adelante
    },

    setTheme(theme) {
      document.body.className = `theme-${theme}`;
      this.addLog(`Tema cambiado a ${theme}`);
    }
  }
}