"""Configuration for Aerial Person Detection App - LEGACY (Use src/config.py instead)"""
import os

# Model configuration
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "YOLOv8_Aerial_Person_Detection/YOLOv8_Aerial_Person_Detection/runs/aerial_person_detection/weights/best.pt"
)
INPUT_SIZE = 640
CONF_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# Classes - All 12 detectable classes from trained model
CLASSES = [
    "awning-tricycle",
    "bicycle",
    "bus",
    "car",
    "ignored regions",
    "motor",
    "others",
    "pedestrian",
    "people",
    "tricycle",
    "truck",
    "van"
]

# UI configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MAX_VIDEO_FPS = 30
