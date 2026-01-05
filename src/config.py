"""Application Configuration"""
import json
import os
from pathlib import Path
from typing import Dict, Any

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
MODEL_DIR = PROJECT_ROOT / "YOLOv8_Aerial_Person_Detection" / "YOLOv8_Aerial_Person_Detection" / "runs" / "aerial_person_detection" / "weights"
MODEL_PATH = MODEL_DIR / "best.pt"  # Using PyTorch format instead of ONNX
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_FILE = PROJECT_ROOT / "app_settings.json"

# Create directories if not exist
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Model Configuration
MODEL_CONFIG = {
    "input_size": 640,
    "confidence_threshold": 0.5,
    "iou_threshold": 0.45,
    "classes": ["person"],
    "num_classes": 1,
}

# UI Configuration
UI_CONFIG = {
    "window_width": 1600,
    "window_height": 1000,
    "theme": "dark",  # "light" or "dark"
}

# Video Configuration
VIDEO_CONFIG = {
    "max_fps": 30,
    "frame_skip": 1,  # Process every nth frame
    "output_fps": 24,
    "codec": "mp4v",
}

# Color map for classes (BGR format for OpenCV)
CLASS_COLORS = {
    "person": (0, 255, 0),  # Green
}

# Default settings
DEFAULT_SETTINGS = {
    "confidence_threshold": 0.5,
    "iou_threshold": 0.45,
    "show_bboxes": True,
    "show_labels": True,
    "show_confidence": True,
    "show_count": True,
    "frame_skip": 1,
    "theme": "dark",
    "side_by_side": True,
}


class Settings:
    """Settings manager with JSON persistence"""
    
    def __init__(self):
        self.data: Dict[str, Any] = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from JSON file or use defaults"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return DEFAULT_SETTINGS.copy()
    
    def save(self) -> None:
        """Save settings to JSON file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default=None) -> Any:
        """Get setting value"""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set setting value"""
        self.data[key] = value
        self.save()
    
    def update(self, **kwargs) -> None:
        """Update multiple settings"""
        self.data.update(kwargs)
        self.save()


# Global settings instance
settings = Settings()
