"""PyTorch Model Inference Engine"""
import cv2
import numpy as np
from typing import List, Tuple, Dict, Any
from pathlib import Path
from ultralytics import YOLO

from src.config import MODEL_PATH, MODEL_CONFIG, CLASS_COLORS


class Detection:
    """Detection result container"""
    
    def __init__(self, box: Tuple[int, int, int, int], confidence: float, class_id: int, class_name: str):
        self.box = box  # (x1, y1, x2, y2)
        self.confidence = confidence
        self.class_id = class_id
        self.class_name = class_name
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "box": self.box,
            "confidence": float(self.confidence),
            "class_id": self.class_id,
            "class_name": self.class_name,
        }


class AerialDetector:
    """PyTorch-based aerial person detector"""
    
    def __init__(self, model_path: Path = MODEL_PATH):
        """Initialize detector with PyTorch model"""
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Load YOLO model from local file
        self.model = YOLO(str(model_path))
        
        # Configuration
        self.input_size = MODEL_CONFIG["input_size"]
        self.conf_threshold = MODEL_CONFIG["confidence_threshold"]
        self.iou_threshold = MODEL_CONFIG["iou_threshold"]
        self.classes = MODEL_CONFIG["classes"]
    
    def set_thresholds(self, conf: float, iou: float) -> None:
        """Update detection thresholds"""
        self.conf_threshold = max(0.0, min(1.0, conf))
        self.iou_threshold = max(0.0, min(1.0, iou))
    
    def detect(self, image: np.ndarray) -> List[Detection]:
        """Run detection on image"""
        # Inference with YOLO (handles preprocessing internally)
        results = self.model(image, conf=self.conf_threshold, iou=self.iou_threshold, verbose=False)
        
        detections = []
        if results and len(results) > 0:
            result = results[0]
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                cls_id = int(box.cls[0].cpu().numpy())
                cls_name = result.names.get(cls_id, f"Class {cls_id}")
                
                detection = Detection(
                    box=(int(x1), int(y1), int(x2), int(y2)),
                    confidence=float(conf),
                    class_id=cls_id,
                    class_name=cls_name
                )
                detections.append(detection)
        
        return detections
    
    @staticmethod
    def draw_detections(
        image: np.ndarray,
        detections: List[Detection],
        show_boxes: bool = True,
        show_labels: bool = True,
        show_confidence: bool = True,
    ) -> np.ndarray:
        """Draw detections on image"""
        result = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det.box
            
            if show_boxes:
                color = CLASS_COLORS.get(det.class_name, (0, 255, 0))
                cv2.rectangle(result, (x1, y1), (x2, y2), color, 2)
            
            if show_labels or show_confidence:
                label = det.class_name
                if show_confidence:
                    label += f": {det.confidence:.2f}"
                
                color = CLASS_COLORS.get(det.class_name, (0, 255, 0))
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.rectangle(
                    result,
                    (x1, y1 - label_size[1] - 6),
                    (x1 + label_size[0] + 4, y1),
                    color,
                    -1
                )
                cv2.putText(
                    result,
                    label,
                    (x1 + 2, y1 - 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 0),
                    2
                )
        
        return result
