# ⚡ QUICK REFERENCE - Aerial Detection App

## 🚀 Start Application
```bash
python app.py
```

## 📁 Project Structure at a Glance
```
app.py                     ← Run this
src/config.py             ← Settings
src/core/detector.py      ← AI Engine  
src/core/media_handler.py ← File I/O
src/ui/main_window.py     ← GUI
src/utils/worker.py       ← Threading
```

## 🎯 Basic Workflow

### Process Image
1. 📷 Open Image → Select JPG/PNG
2. 🚀 Run Detection → Wait for completion
3. 💾 Save Image → Export to outputs/

### Process Video
1. 🎬 Open Video → Select MP4/AVI
2. Set Frame Skip (1=all, 3=every 3rd frame)
3. 🚀 Run Detection → Watch progress
4. 💾 Save Video → Export MP4

## ⚙️ Settings Panel (Right Sidebar)

**Detection Settings:**
- Confidence Threshold: 0.0-1.0 (higher = fewer detections)
- IOU Threshold: 0.0-1.0 (NMS overlap filtering)

**Visualization:**
- ✓ Show Bounding Boxes
- ✓ Show Class Labels
- ✓ Show Confidence Scores
- ✓ Show Count Overlay

**Video Options:**
- Frame Skip: 1-30 (process every nth frame)

## 📊 Statistics Panel (Left Sidebar)

- **Objects**: Total detections in current frame/image
- **Person**: Count of person detections

## 💾 Output Locations

All files saved to: `outputs/` folder
- Images: `image_name_detected.png`
- Videos: `video_name_detected.mp4`

Open folder: Click "📂 Open Outputs Folder"

## 🔧 Configuration Files

**app_settings.json** (auto-created)
- Saves all your settings between sessions
- Edit manually to reset defaults

**src/config.py**
- Model path and specifications
- Default thresholds
- Color mapping for classes
- UI dimensions

## 📈 Performance Tips

| Action | Impact |
|--------|--------|
| Increase frame skip | 3-5x faster video processing |
| Lower confidence | Faster (fewer detections to filter) |
| Use GPU | 5-10x faster than CPU |
| Resize input | Faster preprocessing |

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| Slow processing | Enable GPU / Increase frame skip |
| Model not found | Check path in src/config.py |
| Import errors | pip install -r requirements.txt |
| UI freezes | Normal - processing in background |

## 🎨 UI Layout

```
┌─────────────────────────────────────────┐
│  🦅 Aerial Person Detection             │
├────────────┬──────────────┬─────────────┤
│            │              │             │
│  CONTROLS  │  PREVIEW     │  SETTINGS   │
│            │  AREA        │             │
│  • Open    │  (Image/     │  • Thresholds
│  • Process │   Video)     │  • Show/Hide
│  • Save    │              │  • Video opts
│            │              │  • Stats     │
└────────────┴──────────────┴─────────────┘
```

## 🔌 Model Specifications

- **Type**: YOLOv8 Nano (ONNX)
- **Input**: 640×640 RGB image
- **Output**: Bounding boxes + confidence
- **Classes**: Person
- **Speed**: ~20ms per frame (GPU)

## 📦 Install Dependencies

```bash
# Create virtual environment (first time only)
python -m venv .venv
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## 🎓 Code Examples

### Detect persons in image (no GUI)
```python
from src.core.detector import AerialDetector
from src.core.media_handler import MediaHandler
from pathlib import Path

detector = AerialDetector()
image = MediaHandler.load_image(Path("photo.jpg"))
detections = detector.detect(image)

for det in detections:
    print(f"Person at {det.box} ({det.confidence:.2f}%)")
```

### Change thresholds programmatically
```python
detector.set_thresholds(conf=0.6, iou=0.5)
```

### Process image with settings
```python
annotated = detector.draw_detections(
    image, 
    detections,
    show_boxes=True,
    show_labels=True,
    show_confidence=True
)
```

## 📚 Documentation Files

- **README.md** - Full features and usage guide
- **SETUP.md** - Installation and troubleshooting
- **PROJECT_SUMMARY.md** - Architecture and design
- **QUICK_REFERENCE.md** - This file!

## ✨ Keyboard Shortcuts (Future)

Currently all via mouse click. Shortcuts planned for future versions.

## 🚧 Known Limitations

- ✗ Webcam support (coming soon)
- ✗ Light theme (dark only, for now)
- ✗ Batch processing UI (available via API)
- ✗ Custom model loading (must edit config.py)

## 📞 Quick Help

1. **Can't find model?**
   - Check: `YOLOv8_Aerial_Person_Detection/.../weights/best.onnx`

2. **Processing slow?**
   - Enable GPU or increase frame skip

3. **Detections missing?**
   - Lower confidence threshold to 0.3-0.4

4. **App won't start?**
   - Verify: `python -m pip install -r requirements.txt`

5. **Can't save output?**
   - Check write permissions in outputs/ folder

## 🎯 Next Steps

1. ✓ Install and run: `python app.py`
2. ✓ Process first image (test with aerial photo)
3. ✓ Adjust settings and explore
4. ✓ Try video processing
5. ✓ Export and save results

---

**Need more help?** See README.md or SETUP.md
