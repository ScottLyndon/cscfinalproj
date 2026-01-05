# 🦅 Aerial Person Detection Desktop App

A professional PyQt5-based desktop application for object detection in aerial images and videos using YOLOv8 PyTorch model with ultralytics. Features real-time inference, batch processing, and exportable annotated outputs.

## ✨ Features

### Input
- 📁 **File Browser**: Drag-and-drop or file picker for images/videos
- 📷 **Image Formats**: JPG, PNG, BMP, TIFF
- 🎬 **Video Formats**: MP4, AVI, MOV, MKV, FLV, WMV
- 👁️ **Preview**: Real-time preview before/after processing

### AI Processing
- 🤖 **Object Detection**: PyTorch-powered person detection (YOLOv8 Nano)
- 🎯 **Configurable Thresholds**: Confidence and IOU adjustable via sliders
- ⚡ **GPU Support**: CUDA acceleration with CPU fallback
- 🔄 **Frame-by-frame Inference**: Video processing with frame skip option

### Visualization
- 📦 **Bounding Boxes**: Color-coded detection boxes
- 🏷️ **Labels**: Class names with confidence scores
- 👥 **Count Overlay**: Real-time object count display
- 🔀 **Side-by-Side View**: Original vs annotated comparison
- 📊 **Statistics Panel**: Live detection count tracking

### Output
- 💾 **Save Images**: Export annotated images (PNG, JPG)
- 🎥 **Save Videos**: Export annotated videos (MP4)
- 📂 **Batch Output**: Store in organized output folder
- 📋 **Metadata**: Detection stats with each output

### UI/UX
- 🎨 **Dark Theme**: Professional dark interface (light theme coming soon)
- 📱 **Responsive Layout**: Sidebar + preview + settings
- ⚙️ **Settings Panel**: All controls in organized sidebar
- 📈 **Progress Tracking**: Real-time progress bar for batch operations
- ⌨️ **Keyboard Shortcuts**: Quick access to common functions
- ♿ **Accessible**: High contrast, readable fonts

## 🚀 Quick Start

### Requirements
- **Python 3.11** (recommended)
- **Windows/Linux/macOS**
- **2GB+ free disk space** for model and outputs

### Installation

1. **Clone/Navigate to project**:
```bash
cd eagleswings
```

2. **Create virtual environment** (recommended):
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

## 📖 Usage Guide

### Processing Images

1. Click **📷 Open Image**
2. Select an image file (JPG, PNG, BMP, TIFF)
3. Preview appears in center panel
4. Click **🚀 Run Detection** to process
5. View statistics in right panel
6. Click **💾 Save Image** to export annotated version

### Processing Videos

1. Click **🎬 Open Video**
2. Select a video file (MP4, AVI, MOV, MKV)
3. First frame appears in preview
4. Click **🚀 Run Detection** to process all frames
5. Watch progress bar (can skip frames for speed)
6. Click **💾 Save Video** to export annotated version

### Adjusting Detection Settings

**Confidence Threshold**: 
- Higher = fewer, more confident detections
- Lower = more detections (may include false positives)
- Recommended: 0.4-0.6

**IOU Threshold**:
- Controls duplicate box filtering
- Higher = keep more overlapping boxes
- Recommended: 0.4-0.5

**Visualization Options**:
- ✓ Show Bounding Boxes
- ✓ Show Class Labels
- ✓ Show Confidence Scores
- ✓ Show Count Overlay

**Video Options**:
- Frame Skip: Process every nth frame (1 = all frames, 2 = every 2nd frame)
- Higher skip = faster but less comprehensive

## 📁 Project Structure

```
eagleswings/
├── app.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
│
├── src/
│   ├── config.py                   # Configuration & settings management
│   ├── __init__.py
│   │
│   ├── core/                       # AI inference & media processing
   │   ├── detector.py             # PyTorch inference engine (ultralytics YOLO)
│   │   ├── media_handler.py        # Image/video I/O
│   │   └── __init__.py
│   │
│   ├── ui/                         # User interface
│   │   ├── main_window.py          # Main application window
│   │   └── __init__.py
│   │
│   └── utils/                      # Utilities
│       ├── worker.py               # Threading for async processing
│       └── __init__.py
│
├── YOLOv8_Aerial_Person_Detection/ # Model directory
│   └── YOLOv8_Aerial_Person_Detection/
│       └── runs/aerial_person_detection/
│           └── weights/
│               ├── best.pt         # ← PyTorch model (used by app)
│               └── ...
│
├── outputs/                        # Generated detections (auto-created)
│   ├── image_detected.png
│   ├── video_detected.mp4
│   └── ...
│
└── assets/                         # UI assets (icons, etc.)
```

## ⚙️ Configuration

Settings are saved to `app_settings.json`:

```json
{
  "confidence_threshold": 0.5,
  "iou_threshold": 0.45,
  "show_bboxes": true,
  "show_labels": true,
  "show_confidence": true,
  "show_count": false,
  "frame_skip": 1,
  "theme": "dark",
  "side_by_side": true
}
```

### Model Config (src/config.py)

```python
MODEL_CONFIG = {
    "input_size": 640,
    "confidence_threshold": 0.5,
    "iou_threshold": 0.45,
    "classes": ["person"],
    "num_classes": 1,
}
```

## 📊 Model Specifications

- **Framework**: YOLOv8 Nano
- **Format**: PyTorch (.pt)
- **Backend**: ultralytics YOLO
- **Input**: 640×640 RGB image
- **Output**: Bounding boxes + confidence scores
- **Classes**: Person
- **Inference Time**: ~10-25ms per frame (GPU), ~30-50ms (CPU)
- **Model Size**: ~6MB (.pt)

## 🔧 Troubleshooting

### "Model not found" Error
```
✗ FileNotFoundError: Model not found
```
**Solution**: Ensure model file exists at:
```
YOLOv8_Aerial_Person_Detection/YOLOv8_Aerial_Person_Detection/runs/
aerial_person_detection/weights/best.pt
```

### Slow Processing
- Use GPU: Install CUDA 11.8+ for NVIDIA cards
- Increase frame skip for videos
- Close other applications
- Ensure Python 3.11+ is installed

### Memory Issues
- Reduce frame skip (process fewer frames)
- Use smaller input videos
- Increase available RAM

### "No module named" Errors
```bash
# Verify virtual environment is activated
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

### UI Not Responsive During Processing
- This is normal - processing happens in background thread
- Watch progress bar for completion
- Click ⏹️ Stop to cancel

## 🎨 Customization

### Change Confidence Threshold Programmatically
```python
from src.core.detector import AerialDetector

detector = AerialDetector()
detector.set_thresholds(conf=0.6, iou=0.5)
```

### Process Images Without GUI
```python
from src.core.detector import AerialDetector
from src.core.media_handler import MediaHandler
from pathlib import Path

detector = AerialDetector()
image = MediaHandler.load_image(Path("image.jpg"))
detections = detector.detect(image)

for det in detections:
    print(f"Person at {det.box} (confidence: {det.confidence:.2f})")
```

### Add Custom Classes
Edit `src/config.py`:
```python
MODEL_CONFIG = {
    ...
    "classes": ["person", "car", "bike"],  # Add more classes
    ...
}
```

## 🚀 Performance Tips

| Setting | Impact | Recommendation |
|---------|--------|-----------------|
| Confidence Threshold | Detections | 0.5 for balanced |
| Frame Skip | Speed | 2-5 for videos |
| GPU Support | Speed | ✓ Enable if available |
| Input Size | Quality | 640×640 (default) |

## 📦 Dependencies

**Key Packages:**
- **ultralytics** (8.0.238): YOLO model loader and inference
- **torch** (2.1.2): PyTorch deep learning framework
- **torchvision** (0.16.2): Vision utilities for PyTorch
- **opencv-python** (4.8.1.78): Image/video processing
- **numpy** (≥1.24.3, <2.0): Numerical computing
- **PyQt5** (5.15.9): GUI framework
- **Pillow** (10.1.0): Image I/O

| Package | Version | Purpose |
|---------|---------|---------|
| ultralytics | 8.0.238 | YOLO model & inference |
| torch | 2.1.2 | PyTorch framework |
| torchvision | 0.16.2 | Vision utilities |
| opencv-python | 4.8.1.78 | Image/video processing |
| numpy | ≥1.24.3,<2.0 | Numerical computing |
| PyQt5 | 5.15.9 | GUI framework |
| Pillow | 10.1.0 | Image I/O |

## 🔄 Workflow Examples

### Example 1: Detect Persons in Drone Photo
1. Click 📷 Open Image → select drone photo
2. Set Confidence to 0.5
3. Click 🚀 Run Detection
4. Click 💾 Save Image → save to outputs/
5. Open outputs/ folder to view annotated image

### Example 2: Process Aerial Video
1. Click 🎬 Open Video → select aerial video
2. Set Frame Skip to 3 (skip 2 frames, process 1)
3. Set Show Count Overlay ✓
4. Click 🚀 Run Detection
5. Watch progress bar
6. Click 💾 Save Video → export MP4

## 📝 License

Project includes YOLOv8 Aerial Person Detection model.
See model folder for license details.

## 🐛 Known Limitations

- Webcam support (coming soon)
- Export to formats other than PNG/MP4 (expandable)
- Batch processing UI (available via API)

## 💡 Future Enhancements

- [ ] Real-time webcam detection
- [ ] Multiple model support
- [ ] Video streaming input
- [ ] REST API endpoint
- [ ] Batch processing queue
- [ ] Object tracking across frames
- [ ] Export to COCO/Pascal VOC formats
- [ ] Light theme option

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review model path configuration
3. Verify Python 3.11+ installation
4. Check GPU drivers if using CUDA
