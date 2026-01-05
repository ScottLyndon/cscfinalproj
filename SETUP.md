"""
SETUP INSTRUCTIONS - Aerial Detection Desktop App

This file contains step-by-step instructions to set up and run the application.
"""

# ============================================================================
# SYSTEM REQUIREMENTS
# ============================================================================

- Python 3.11 (recommended) or Python 3.10+
- Windows 10/11, Linux (Ubuntu 20.04+), or macOS 11+
- 4GB RAM minimum (8GB+ recommended for video processing)
- 2GB disk space for model and dependencies
- NVIDIA GPU (optional, for faster processing with CUDA)

# ============================================================================
# INSTALLATION STEPS
# ============================================================================

## Step 1: Set Up Python Environment

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate


## Step 2: Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt


## Step 3: Verify Model File

Check that the model file exists:
  Path: YOLOv8_Aerial_Person_Detection/YOLOv8_Aerial_Person_Detection/runs/aerial_person_detection/weights/best.onnx
  
If not found:
  1. Re-download the model folder
  2. Extract to project root
  3. Ensure folder structure matches above path


## Step 4: Run Application

python app.py

The GUI window should appear with:
- Left sidebar: Input controls, processing, output options
- Center: Image/video preview area
- Right sidebar: Detection settings and visualization options


# ============================================================================
# COMMON SETUP ISSUES & SOLUTIONS
# ============================================================================

### Issue 1: "No module named 'PyQt5'"
Solution:
  - Ensure .venv is activated
  - Run: pip install PyQt5==5.15.10

### Issue 2: "ONNX Runtime failed to import"
Solution:
  - Run: pip install onnxruntime==1.18.0
  - For GPU support: pip install onnxruntime-gpu==1.18.0

### Issue 3: "Model not found"
Solution:
  - Check file path in src/config.py
  - Verify best.onnx exists in:
    YOLOv8_Aerial_Person_Detection/.../ weights/best.onnx

### Issue 4: "Python version error"
Solution:
  - Check Python version: python --version
  - Use Python 3.11+
  - If needed, install: https://www.python.org/downloads/

### Issue 5: "OpenCV import error"
Solution:
  - Run: pip install opencv-python==4.9.0.80


# ============================================================================
# FIRST RUN CHECKLIST
# ============================================================================

□ Python 3.11+ installed
□ Virtual environment created and activated
□ Requirements installed (pip install -r requirements.txt)
□ Model file exists at correct path
□ No import errors when running: python app.py
□ Application window appears
□ Can load test image/video without errors


# ============================================================================
# GPU ACCELERATION (OPTIONAL)
# ============================================================================

For faster processing with NVIDIA GPU:

1. Install CUDA 11.8+
   - Download from: https://developer.nvidia.com/cuda-downloads

2. Install cuDNN 8.0+
   - Download from: https://developer.nvidia.com/cudnn

3. Reinstall ONNX Runtime with GPU support:
   pip uninstall onnxruntime
   pip install onnxruntime-gpu==1.18.0

4. Verify GPU is used:
   - First detection should take ~15-30ms (vs 50-200ms on CPU)


# ============================================================================
# DEVELOPMENT NOTES
# ============================================================================

## Code Structure

src/
├── config.py          # All configuration in one place
├── core/
│   ├── detector.py    # ONNX inference engine
│   └── media_handler.py  # Image/video I/O
├── ui/
│   └── main_window.py # PyQt5 interface
└── utils/
    └── worker.py      # Background processing thread

## Adding Custom Models

1. Place ONNX model in: models/ folder
2. Update config.py with new model path
3. Update MODEL_CONFIG with model specifications
4. Adjust preprocessing if needed in detector.py

## Extending with New Features

Example: Add face detection

1. Add to config.py:
   "num_classes": 2,
   "classes": ["person", "face"],

2. Update detector.py postprocessing if needed

3. Add UI controls in main_window.py SettingsPanel

4. Update class_colors in config.py for visualization


## Type Hints

All functions use type hints for better IDE support.
Example:
  def detect(self, image: np.ndarray) -> List[Detection]:

## Testing

Run individual modules:
  python -c "from src.core.detector import AerialDetector; print('OK')"
  python -c "from src.ui.main_window import MainWindow; print('OK')"


# ============================================================================
# PERFORMANCE OPTIMIZATION
# ============================================================================

1. Use GPU if available
2. Increase frame skip for videos (skip 2-3 frames for 3x speedup)
3. Reduce confidence threshold for speed (fewer NMS calculations)
4. Close background applications
5. Use SSD drives instead of HDD

## Benchmark Times (per frame, 640x640):
- CPU (Intel i5): ~120ms per frame
- GPU (NVIDIA RTX 3060): ~20ms per frame
- GPU (NVIDIA A100): ~5ms per frame


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

### Example 1: Process single image
1. Click "📷 Open Image"
2. Select image.jpg
3. Click "🚀 Run Detection"
4. Click "💾 Save Image"
5. Find output in outputs/ folder

### Example 2: Process video
1. Click "🎬 Open Video"
2. Select video.mp4
3. Set frame skip to 3 (faster)
4. Click "🚀 Run Detection"
5. Click "💾 Save Video"
6. Wait for processing to complete


# ============================================================================
# SUPPORT & TROUBLESHOOTING
# ============================================================================

1. Check README.md for detailed documentation
2. Review logs in terminal output
3. Check app_settings.json for configuration issues
4. Ensure model file integrity

For issues:
- Verify Python 3.11+
- Reinstall requirements: pip install -r requirements.txt --force-reinstall
- Clear cache: rm -rf __pycache__ .pytest_cache
