## 🧩 Disposición general de la ventana

- **Cabecera**: título, versión, selector de idioma (`EN`/`ES`/etc.) y selector de tema (`Matrix`, `Ámbar`, `Dracula`…).
- **Columna izquierda (25%)**: recuadro de la mascota con su diálogo dinámico. Puede cambiar de expresión según el contexto.
- **Columna derecha (75%)**: área principal donde se muestran los archivos arrastrados, las opciones de conversión, selector de formato, ruta de exportación y botón de acción.
- **Panel inferior**: registro de logs (historial de eventos, errores, sugerencias de la mascota).

Todos los controles se operan con el ratón (clic) o con atajos de teclado (mostrados en la interfaz).

---

## 🖼️ Boceto 1 – Pantalla de inicio (sin archivos)

```
┌────────────────────────────────────────────────────────────────────────────┐
│ MorphoTheConverter v1.0                               [EN ▼] [Matrix ▼]   │
├──────────────────────────────┬─────────────────────────────────────────────┤
│ ┌──────────────────────────┐ │ ┌─────────────────────────────────────────┐ │
│ │       ◤M◥                │ │ │            ZONA DE ARRASTRE             │ │
│ │  ┌────────────────────┐  │ │ │                                         │ │
│ │  │ ¡Hola! Soy Morpho. │  │ │ │   Arrastra aquí archivos o carpetas    │ │
│ │  │ Arrastra cualquier │  │ │ │      o presiona [O] para abrir         │ │
│ │  │ archivo para ver   │  │ │ │                                         │ │
│ │  │ las conversiones   │  │ │ │   Formatos soportados:                 │ │
│ │  │ disponibles.       │  │ │ │   🖼️ PNG, JPG, WebP, DDS...            │ │
│ │  └────────────────────┘  │ │ │   🔊 WAV, MP3, OGG, FLAC...            │ │
│ │                          │ │ │   🎬 MP4, MKV, WEBM...                  │ │
│ └──────────────────────────┘ │ └─────────────────────────────────────────┘ │
│                              │                                             │
│                              │  📁 Exportar en: [origen/_converted ▼]     │
│                              │  🎯 Formato por defecto: [Automático ▼]    │
│                              │  [ ▶ CONVERTIR ] (deshabilitado)           │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ [Logs]                                                                      │
│ > Sistema listo. Esperando archivos...                                     │
│ > Morpho: Puedes arrastrar múltiples archivos o una carpeta entera.        │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖼️ Boceto 2 – Un solo archivo (imagen PNG)

```
┌────────────────────────────────────────────────────────────────────────────┐
│ MorphoTheConverter v1.0                               [EN ▼] [Matrix ▼]   │
├──────────────────────────────┬─────────────────────────────────────────────┤
│ ┌──────────────────────────┐ │ ┌─────────────────────────────────────────┐ │
│ │       ◤M◥                │ │ │  📄 archivo.png                          │ │
│ │  ┌────────────────────┐  │ │ │     Tipo: Imagen (PNG)                  │ │
│ │  │ He detectado una   │  │ │ │     Tamaño: 2.3 MB                       │ │
│ │  │ imagen PNG. Puedo  │  │ │ │                                         │ │
│ │  │ convertirla a:     │  │ │ │  Opciones:                              │ │
│ │  │ • WebP (reducido)  │  │ │ │  ○ WebP (recomendado)                   │ │
│ │  │ • JPG              │  │ │ │  ○ JPG                                  │ │
│ │  │ • DDS (para GPU)   │  │ │ │  ● DDS (para texturas de juego)         │ │
│ │  │ ¿Qué formato usas? │  │ │ │  ○ TGA                                  │ │
│ │  └────────────────────┘  │ │ │                                         │ │
│ │                          │ │ │  📁 Exportar en: [origen/_converted ▼]  │ │
│ └──────────────────────────┘ │ │  [ ▶ CONVERTIR ]                        │ │
│                              │ └─────────────────────────────────────────┘ │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ [Logs]                                                                      │
│ > Archivo imagen.png cargado.                                              │
│ > Morpho: DDS es ideal para motores como Unity o Godot.                    │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖼️ Boceto 3 – Múltiples archivos de distintos tipos

```
┌────────────────────────────────────────────────────────────────────────────┐
│ MorphoTheConverter v1.0                               [EN ▼] [Matrix ▼]   │
├──────────────────────────────┬─────────────────────────────────────────────┤
│ ┌──────────────────────────┐ │ ┌─────────────────────────────────────────┐ │
│ │       ◤M◥                │ │ │  Archivos seleccionados (3):             │ │
│ │  ┌────────────────────┐  │ │ │  🖼️ hero.png (imagen)                    │ │
│ │  │ Hay varios tipos.  │  │ │ │  🔊 boss.mp3 (audio)                     │ │
│ │  │ Puedes convertirlos │  │ │ │  🎬 trailer.mp4 (video)                  │ │
│ │  │ al mismo formato    │  │ │ │                                         │ │
│ │  │ (si tienen soporte) │  │ │ │  Conversión por lotes:                  │ │
│ │  │ o elegir por tipo.  │  │ │ │  [x] Usar formato unificado: [WebP ▼]  │ │
│ │  │ Te recomiendo:      │  │ │ │  ○ Por tipo:                            │ │
│ │  │ - Imagen → WebP     │  │ │ │    Imagen: [WebP ▼]  Audio: [OGG ▼]    │ │
│ │  │ - Audio → OGG       │  │ │ │    Video:  [WEBM ▼]                     │ │
│ │  │ - Video → WEBM      │  │ │ │                                         │ │
│ │  └────────────────────┘  │ │ │  📁 Exportar en: [origen/_converted ▼]  │ │
│ └──────────────────────────┘ │ │  [ ▶ CONVERTIR TODOS ]                  │ │
│                              │ └─────────────────────────────────────────┘ │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ [Logs]                                                                      │
│ > 3 archivos cargados. Detectados: 1 imagen, 1 audio, 1 video.             │
│ > Morpho: Para juegos, WebP, OGG y WEBM son formatos ligeros y compatibles.│
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖼️ Boceto 4 – Carpeta completa arrastrada

```
┌────────────────────────────────────────────────────────────────────────────┐
│ MorphoTheConverter v1.0                               [EN ▼] [Matrix ▼]   │
├──────────────────────────────┬─────────────────────────────────────────────┤
│ ┌──────────────────────────┐ │ ┌─────────────────────────────────────────┐ │
│ │       ◤M◥                │ │ │  📁 Carpeta: "assets/"                   │ │
│ │  ┌────────────────────┐  │ │ │  Contenido escaneado:                    │ │
│ │  │ Has arrastrado una │  │ │ │  🖼️ 45 imágenes (PNG, JPG)               │ │
│ │  │ carpeta. Voy a     │  │ │ │  🔊 12 audios (WAV, MP3)                 │ │
│ │  │ escanear todos los │  │ │ │  🎬 3 videos (MP4)                       │ │
│ │  │ archivos           │  │ │ │  📄 8 documentos (MD, TXT)               │ │
│ │  │ compatibles.       │  │ │ │                                         │ │
│ │  │ ¿Procesamos todo?  │  │ │ │  Opciones:                               │ │
│ │  │ Te sugiero usar    │  │ │ │  [✓] Incluir subcarpetas                 │ │
│ │  │ filtros para no    │  │ │ │  Filtrar por tipo: [Todos ▼]            │ │
│ │  │ mezclar formatos.  │  │ │ │  Formato destino: [Preservar original ▼]│ │
│ │  └────────────────────┘  │ │ │                                         │ │
│ └──────────────────────────┘ │ │  📁 Exportar en: [misma estructura ▼]    │ │
│                              │ │  [ ▶ CONVERTIR CARPETA ]                 │ │
│                              │ └─────────────────────────────────────────┘ │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ [Logs]                                                                      │
│ > Escaneando... 68 archivos compatibles encontrados.                       │
│ > Morpho: Puedes convertir solo imágenes si quieres. Los documentos necesitan Pandoc. │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖼️ Boceto 5 – Error (binario externo faltante)

```
┌────────────────────────────────────────────────────────────────────────────┐
│ MorphoTheConverter v1.0                               [EN ▼] [Matrix ▼]   │
├──────────────────────────────┬─────────────────────────────────────────────┤
│ ┌──────────────────────────┐ │ ┌─────────────────────────────────────────┐ │
│ │       ◤M◥                │ │ │  ❌ Error al convertir audio.mp3        │ │
│ │  ┌────────────────────┐  │ │ │                                         │ │
│ │  │ ¡Oh no! No         │  │ │ │  No se encuentra 'ffmpeg' en            │ │
│ │  │ encuentro 'ffmpeg' │  │ │ │  bin/linux/.                             │ │
│ │  │ en la carpeta bin/.│  │ │ │                                         │ │
│ │  │ Por favor,         │  │ │ │  Solución:                               │ │
│ │  │ descárgalo y       │  │ │ │  [📥 Descargar FFmpeg]                   │ │
│ │  │ colócalo allí, o   │  │ │ │  [📂 Abrir carpeta bin]                  │ │
│ │  │ revisa tu          │  │ │ │                                         │ │
│ │  │ instalación.       │  │ │ │  Puedes continuar con otros archivos.   │ │
│ │  └────────────────────┘  │ │ │                                         │ │
│ └──────────────────────────┘ │ └─────────────────────────────────────────┘ │
│                              │                                             │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ [Logs]                                                                      │
│ > [ERROR] Al convertir audio.mp3: falta el binario ffmpeg.                │
│ > Morpho sugiere descargar las dependencias desde la documentación.        │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖼️ Boceto 6 – Menú de configuración (idioma / tema)

Al hacer clic en el selector de idioma (por ejemplo `[EN ▼]`), se despliega una lista en estilo terminal:

```
┌────────────────────────────────────────────────────────────────────────────┐
│ MorphoTheConverter v1.0                               [EN ▼] [Matrix ▼]   │
│                                                        ┌────────┐          │
│                                                        │ EN     │          │
│                                                        │ ES     │          │
│                                                        │ JA     │          │
│                                                        └────────┘          │
├──────────────────────────────┬─────────────────────────────────────────────┤
...
```

De manera similar para el selector de tema (`Matrix ▼`), ofreciendo opciones como `Matrix (verde)`, `Ámbar`, `Dracula`, `Solarized`, `Claro`.

---

## 🧠 Comportamiento dinámico de la mascota

La mascota **Morpho** reacciona en tiempo real según la acción del usuario:

| Situación | Diálogo ejemplo |
|-----------|----------------|
| Sin archivos | *"Arrastra algo o presiona [O] para abrir."* |
| Un archivo imagen | *"Puedo convertir esto a WebP, JPG o DDS. ¿Cuál prefieres?"* |
| Un archivo audio | *"Para música en juegos, OGG con bucle es ideal. ¿Te ayudo con los metadatos?"* |
| Varios archivos mixtos | *"Hay distintos tipos. Podemos convertir cada grupo a su mejor formato."* |
| Carpeta completa | *"Escanearé todo. ¿Filtramos por tipo de archivo?"* |
| Binario faltante | *"Falta una herramienta externa. Mira la carpeta bin o descárgala."* |
| Conversión exitosa | *"¡Listo! Tus archivos están en la carpeta de salida."* |
| Error de conversión | *"Algo salió mal. Revisa el log para más detalles."* |

La mascota puede cambiar de **expresión** usando pequeños glifos:  

- `◤◡◥` feliz  
- `◤-◥` pensativo  
- `◤>◥` sorprendido  
- `◤x◥` triste o error

---

## 📌 Ubicación de los elementos principales

- **Selector de idioma** → esquina superior derecha del header.  
- **Selector de tema** → a la derecha del idioma.  
- **Mascota** → columna izquierda, fija, con su burbuja de diálogo.  
- **Zona de archivos** → columna derecha, donde se muestran los elementos arrastrados.  
- **Selector de formato de salida** → dentro de la columna derecha, debajo de la lista de archivos.  
- **Selector de directorio de exportación** → justo antes del botón de conversión.  
- **Botón de conversión** → al final de la columna derecha.  
- **Panel de logs** → en la parte inferior, con desplazamiento vertical.
