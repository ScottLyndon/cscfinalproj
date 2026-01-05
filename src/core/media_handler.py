"""Media Input/Output Handler"""
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Generator
from datetime import datetime

from src.core.detector import Detection, AerialDetector


class MediaHandler:
    """Handle image and video input/output operations"""
    
    SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    SUPPORTED_VIDEOS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}
    
    @staticmethod
    def load_image(image_path: Path) -> Optional[np.ndarray]:
        """Load image from file"""
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        return image
    
    @staticmethod
    def load_video(video_path: Path) -> Tuple[cv2.VideoCapture, dict]:
        """Load video and return capture and metadata"""
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        metadata = {
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "total_frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        }
        
        return cap, metadata
    
    @staticmethod
    def save_image(
        image: np.ndarray,
        output_path: Path,
        quality: int = 95
    ) -> Path:
        """Save annotated image"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if output_path.suffix.lower() in {".jpg", ".jpeg"}:
            cv2.imwrite(str(output_path), image, [cv2.IMWRITE_JPEG_QUALITY, quality])
        else:
            cv2.imwrite(str(output_path), image)
        
        return output_path
    
    @staticmethod
    def save_video(
        frames: List[np.ndarray],
        output_path: Path,
        fps: float = 24,
        codec: str = "mp4v"
    ) -> Path:
        """Save annotated video"""
        if not frames:
            raise ValueError("No frames to save")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        h, w = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (w, h))
        
        for frame in frames:
            writer.write(frame)
        
        writer.release()
        return output_path
    
    @staticmethod
    def process_image(
        image_path: Path,
        detector: AerialDetector,
        show_boxes: bool = True,
        show_labels: bool = True,
        show_confidence: bool = True,
    ) -> Tuple[np.ndarray, List[Detection]]:
        """Process single image"""
        image = MediaHandler.load_image(image_path)
        detections = detector.detect(image)
        annotated = detector.draw_detections(
            image, detections, show_boxes, show_labels, show_confidence
        )
        return annotated, detections
    
    @staticmethod
    def process_video(
        video_path: Path,
        detector: AerialDetector,
        show_boxes: bool = True,
        show_labels: bool = True,
        show_confidence: bool = True,
        frame_skip: int = 1,
        progress_callback=None,
    ) -> Tuple[List[np.ndarray], List[List[Detection]]]:
        """Process video and return frames and detections"""
        cap, metadata = MediaHandler.load_video(video_path)
        
        frames = []
        all_detections = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            if frame_count % frame_skip == 0:
                detections = detector.detect(frame)
                annotated = detector.draw_detections(
                    frame, detections, show_boxes, show_labels, show_confidence
                )
                frames.append(annotated)
                all_detections.append(detections)
            else:
                frames.append(frame)
                all_detections.append([])
            
            if progress_callback:
                progress = int((frame_count / metadata["total_frames"]) * 100)
                progress_callback(progress)
        
        cap.release()
        return frames, all_detections
    
    @staticmethod
    def create_side_by_side(
        original: np.ndarray,
        annotated: np.ndarray
    ) -> np.ndarray:
        """Create side-by-side comparison"""
        # Ensure same height
        h = max(original.shape[0], annotated.shape[0])
        w = original.shape[1] + annotated.shape[1]
        
        # Resize if needed
        orig_resized = cv2.resize(original, (original.shape[1], h)) if original.shape[0] != h else original
        anno_resized = cv2.resize(annotated, (annotated.shape[1], h)) if annotated.shape[0] != h else annotated
        
        # Concatenate
        result = cv2.hconcat([orig_resized, anno_resized])
        
        # Add labels
        cv2.putText(result, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(
            result,
            "Annotated",
            (original.shape[1] + 10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )
        
        return result
    
    @staticmethod
    def add_count_overlay(
        image: np.ndarray,
        detections: List[Detection]
    ) -> np.ndarray:
        """Add detection count overlay"""
        result = image.copy()
        
        # Count by class
        class_counts = {}
        for det in detections:
            class_counts[det.class_name] = class_counts.get(det.class_name, 0) + 1
        
        # Draw count panel
        y_offset = 40
        cv2.putText(result, f"Total: {len(detections)}", (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        for i, (class_name, count) in enumerate(class_counts.items()):
            y_offset += 35
            cv2.putText(result, f"{class_name}: {count}", (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        return result
    
    @staticmethod
    def generate_output_filename(
        input_path: Path,
        suffix: str = "_detected",
        extension: Optional[str] = None
    ) -> Path:
        """Generate output filename"""
        if extension is None:
            extension = input_path.suffix
        
        stem = input_path.stem + suffix
        return input_path.parent / (stem + extension)
