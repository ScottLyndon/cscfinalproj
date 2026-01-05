# 🏗️ ARCHITECTURE DIAGRAM

## Application Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    🦅 AERIAL DETECTION APP                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                        PyQt5 GUI                             │  │
│  │              (src/ui/main_window.py)                        │  │
│  │                                                              │  │
│  │  ┌────────────────┐  ┌─────────────┐  ┌──────────────────┐ │  │
│  │  │ Left Sidebar   │  │   Center    │  │ Right Sidebar    │ │  │
│  │  │ Controls       │  │   Preview   │  │ Settings Panel   │ │  │
│  │  │                │  │   Area      │  │                  │ │  │
│  │  │ • Open Image   │  │             │  │ • Confidence     │ │  │
│  │  │ • Open Video   │  │ [Image/     │  │ • IOU            │ │  │
│  │  │ • Run Process  │  │  Video]     │  │ • Toggle options │ │  │
│  │  │ • Stop         │  │             │  │ • Frame skip     │ │  │
│  │  │ • Save         │  │ Live Preview│  │ • Statistics     │ │  │
│  │  │ • Statistics   │  │             │  │                  │ │  │
│  │  └────────────────┘  └─────────────┘  └──────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                   │                                  │
│                         ┌─────────┴─────────┐                       │
│                         ▼                   ▼                       │
│              ┌─────────────────┐   ┌──────────────────┐             │
│              │   Processing    │   │   Configuration  │             │
│              │    Worker       │   │   Manager        │             │
│              │  (QThread)      │   │  (JSON Settings) │             │
│              │                 │   │                  │             │
│              │ • Background    │   │ • Load defaults  │             │
│              │   processing    │   │ • Save settings  │             │
│              │ • Non-blocking   │   │ • Model paths    │             │
│              │   UI            │   │ • Colors         │             │
│              │ • Progress       │   │ • Thresholds     │             │
│              │   signals       │   │                  │             │
│              └────────┬────────┘   └──────────────────┘             │
│                       │                                              │
│                       ▼                                              │
│         ┌─────────────────────────────┐                            │
│         │   Core Processing Layer     │                            │
│         ├─────────────────────────────┤                            │
│         │                             │                            │
│         │  ┌──────────────────────┐   │                            │
│         │  │ Aerial Detector      │   │                            │
│         │  │ (ONNX Inference)     │   │                            │
│         │  │                      │   │                            │
│         │  │ • Preprocessing      │   │                            │
│         │  │ • ONNX inference     │   │                            │
│         │  │ • Postprocessing     │   │                            │
│         │  │ • NMS filtering      │   │                            │
│         │  │ • Visualization      │   │                            │
│         │  └──────────┬───────────┘   │                            │
│         │             │                │                            │
│         │             ▼                │                            │
│         │  ┌──────────────────────┐   │                            │
│         │  │ Media Handler        │   │                            │
│         │  │ (I/O Operations)     │   │                            │
│         │  │                      │   │                            │
│         │  │ • Load images        │   │                            │
│         │  │ • Load videos        │   │                            │
│         │  │ • Save images        │   │                            │
│         │  │ • Save videos        │   │                            │
│         │  │ • Side-by-side       │   │                            │
│         │  │ • Count overlay      │   │                            │
│         │  └──────────┬───────────┘   │                            │
│         │             │                │                            │
│         └─────────────┼────────────────┘                            │
│                       │                                              │
│                       ▼                                              │
│              ┌──────────────────┐                                  │
│              │  ONNX Runtime    │                                  │
│              │  Inference       │                                  │
│              │                  │                                  │
│              │ • GPU (CUDA)     │                                  │
│              │ • CPU (fallback) │                                  │
│              └────────┬─────────┘                                  │
│                       │                                              │
│                       ▼                                              │
│              ┌──────────────────┐                                  │
│              │ YOLOv8 Model     │                                  │
│              │ (ONNX Format)    │                                  │
│              │ best.onnx        │                                  │
│              │ 640×640 input    │                                  │
│              │ Person detection │                                  │
│              └──────────────────┘                                  │
│                       │                                              │
│                       ▼                                              │
│              ┌──────────────────────────┐                           │
│              │   Detection Results      │                           │
│              │                          │                           │
│              │ • Bounding boxes         │                           │
│              │ • Confidence scores      │                           │
│              │ • Class labels           │                           │
│              │ • Object counts          │                           │
│              │ • Metadata               │                           │
│              └────────────┬─────────────┘                           │
│                           │                                          │
│                           ▼                                          │
│                   ┌──────────────────────┐                          │
│                   │  Visualization &     │                          │
│                   │  Output Export       │                          │
│                   │                      │                          │
│                   │ • Annotated images   │                          │
│                   │ • Annotated videos   │                          │
│                   │ • Side-by-side views │                          │
│                   │ • Count overlays     │                          │
│                   │ • Saved to outputs/  │                          │
│                   └──────────────────────┘                          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
User Input (Image/Video)
    ↓
    ├─→ Load file (media_handler)
    ├─→ Display preview (GUI)
    ├─→ Confirm settings (UI panel)
    ↓
Process Button Clicked
    ├─→ Create worker thread
    ├─→ Start background processing
    ↓
For Each Frame:
    ├─→ Preprocess (normalize, resize)
    ├─→ ONNX inference (GPU/CPU)
    ├─→ Postprocess (NMS, filtering)
    ├─→ Draw detections (boxes, labels)
    ├─→ Update preview (GUI signal)
    ├─→ Update statistics (GUI signal)
    ├─→ Update progress (GUI signal)
    ↓
Processing Complete
    ├─→ Display final frame/image
    ├─→ Show statistics
    ├─→ Enable save buttons
    ↓
User Clicks Save
    ├─→ Save image/video to outputs/
    ├─→ Show success message
    ↓
Done
```

---

## Module Dependencies

```
app.py
  ├─→ src/ui/main_window.py
  │    ├─→ src/config.py (settings, paths)
  │    ├─→ src/core/detector.py (inference)
  │    ├─→ src/core/media_handler.py (I/O)
  │    └─→ src/utils/worker.py (threading)
  │         ├─→ src/core/detector.py
  │         └─→ src/core/media_handler.py
  │
  └─→ PyQt5 (GUI framework)
  
External Dependencies:
  ├─→ onnxruntime (model inference)
  ├─→ opencv-python (image/video processing)
  ├─→ numpy (numerical operations)
  └─→ Pillow (image I/O)
```

---

## File Organization

```
Project Root (eagleswings/)
│
├── Configuration & Docs
│   ├── app.py                 (entry point)
│   ├── requirements.txt        (dependencies)
│   ├── .gitignore            (version control)
│   └── *.md (6 docs)          (documentation)
│
├── Source Code (src/)
│   ├── __init__.py
│   ├── config.py              (configuration)
│   ├── core/                  (AI & media)
│   │   ├── detector.py        (ONNX inference)
│   │   ├── media_handler.py   (file I/O)
│   │   └── __init__.py
│   ├── ui/                    (user interface)
│   │   ├── main_window.py     (PyQt5 app)
│   │   └── __init__.py
│   └── utils/                 (utilities)
│       ├── worker.py          (threading)
│       └── __init__.py
│
├── Model Data
│   └── YOLOv8_Aerial_Person_Detection/
│       └── weights/best.onnx  (model file)
│
└── Runtime Folders
    ├── outputs/               (generated results)
    └── assets/                (UI resources)
```

---

## Class Hierarchy

```
QMainWindow (PyQt5)
  └── MainWindow
       ├── SettingsPanel (QFrame)
       │    └── Settings controls (sliders, checkboxes)
       └── PreviewArea (QFrame)
            └── Image/video display

QThread (PyQt5)
  └── ProcessingWorker
       ├── Signals for progress/completion
       ├── Image processing
       └── Video processing

AerialDetector
  ├── preprocess(image)
  ├── detect(image)
  ├── postprocess(output)
  └── draw_detections(image, detections)

Detection
  ├── box (x1, y1, x2, y2)
  ├── confidence (0-1)
  ├── class_id (int)
  └── class_name (str)

MediaHandler (static utility)
  ├── load_image(path)
  ├── load_video(path)
  ├── save_image(image, path)
  ├── save_video(frames, path)
  ├── process_image(path, detector)
  ├── process_video(path, detector)
  └── add_count_overlay(image, detections)

Settings
  ├── load/save configuration
  ├── JSON persistence
  └── default values
```

---

## Signal Flow (Threading)

```
Main Thread (UI)
  │
  ├─→ User clicks "Run Detection"
  │    │
  │    └─→ Create ProcessingWorker thread
  │         │
  │    ┌────┴─────────────────────────────┐
  │    │                                   │
  │    ▼                                   ▼
  UI Thread                      Worker Thread
  (Blocked?)                     (Processing)
  │                                   │
  │                    ┌──────────────┤
  │                    │              │
  │                    ├─ progress    │ Load frame
  │                    │  signal      │ Detect objects
  │                    │              │ Draw boxes
  │                    ├─ frame_      │ Emit signals
  │                    │  processed   │
  │                    │  signal      │
  │                    │              │
  │                    ├─ finished    │
  │                    │  signal      │
  │                    │              │
  │                    ├─ error       │
  │                    │  signal      │
  │                    │              │
  │                    └──────────────┤
  │                                   │
  ├─ Update progress bar              │
  ├─ Display frame                    │
  ├─ Update statistics                │
  │                                   │
  ▼                         Thread finishes
  Enable save buttons
```

---

## Configuration Hierarchy

```
defaults in config.py
       ↓
   app_settings.json (if exists)
       ↓
   UI settings panel
       ↓
   Active settings
```

**Priority:** UI (highest) → JSON → defaults (lowest)

---

## Processing Pipeline

```
Input Image/Video
  │
  ├─→ Preprocess
  │   ├─ Resize (maintain aspect ratio)
  │   ├─ Pad (center alignment)
  │   ├─ Normalize (0-1 range)
  │   └─ Convert BGR→RGB
  │
  ├─→ ONNX Inference
  │   ├─ Forward pass
  │   ├─ Get output tensor
  │   └─ Return predictions
  │
  ├─→ Postprocess
  │   ├─ Filter by confidence
  │   ├─ Remove padding
  │   ├─ Convert to image coords
  │   └─ Apply NMS
  │
  ├─→ Visualization
  │   ├─ Draw boxes
  │   ├─ Draw labels
  │   ├─ Draw confidence
  │   └─ Optional overlays
  │
  └─→ Output
      ├─ Save image/video
      ├─ Display preview
      └─ Show statistics
```

---

## Performance Optimization Points

```
Input
  ↓
[RESIZE] ← Can optimize size
  ↓
[NORMALIZE] ← Fast with numpy
  ↓
[GPU INFERENCE] ← 15-20ms with GPU, 50-100ms with CPU
  ↓
[NMS FILTERING] ← O(n²) in worst case
  ↓
[VISUALIZATION] ← OpenCV fast
  ↓
[ENCODING] ← Video codec is bottleneck
  ↓
Output
```

**Optimization strategies:**
1. Skip frames (reduce inference count)
2. Lower confidence (fewer NMS iterations)
3. Use GPU (10x faster)
4. Batch processing (future)

---

## Extension Points

```
To add webcam:
  └─→ Modify: ProcessingWorker._process_video()
      └─→ Use: cv2.VideoCapture(0)

To add new model:
  └─→ Update: src/config.py
      ├─→ MODEL_PATH
      ├─→ MODEL_CONFIG
      └─→ CLASS_COLORS

To add new format:
  └─→ Update: media_handler.py
      ├─→ SUPPORTED_IMAGES
      ├─→ SUPPORTED_VIDEOS
      └─→ save_image/save_video methods

To add light theme:
  └─→ Modify: MainWindow.apply_dark_theme()
      └─→ Add: alternative stylesheet

To add batch processing:
  └─→ Extend: ProcessingWorker
      └─→ Add: file queue handling
```

---

This architecture provides:
- ✅ Clean separation of concerns
- ✅ Non-blocking UI during processing
- ✅ Easy extension and customization
- ✅ GPU acceleration support
- ✅ Persistent configuration
- ✅ Professional user interface
