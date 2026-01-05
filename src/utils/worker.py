"""Processing Worker Thread"""
import cv2
from typing import List, Optional, Callable
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal

from src.core.detector import AerialDetector, Detection
from src.core.media_handler import MediaHandler


class ProcessingWorker(QThread):
    """Background worker for image/video processing"""
    
    progress = pyqtSignal(int)  # 0-100
    frame_processed = pyqtSignal(object, list)  # (frame_image, detections)
    finished = pyqtSignal(list)  # all_frames
    error = pyqtSignal(str)
    
    def __init__(self, detector: AerialDetector):
        super().__init__()
        self.detector = detector
        self.is_running = True
        self.media_path: Optional[Path] = None
        self.is_video = False
        self.settings = {}
    
    def set_media(self, media_path: Path, is_video: bool = False):
        """Set media to process"""
        self.media_path = media_path
        self.is_video = is_video
    
    def set_settings(self, **kwargs):
        """Set processing settings"""
        self.settings.update(kwargs)
    
    def run(self):
        """Run processing"""
        try:
            if not self.media_path:
                self.error.emit("No media selected")
                return
            
            if self.is_video:
                self._process_video()
            else:
                self._process_image()
        
        except Exception as e:
            self.error.emit(f"Processing error: {str(e)}")
    
    def _process_image(self):
        """Process single image"""
        try:
            image = MediaHandler.load_image(self.media_path)
            detections = self.detector.detect(image)
            
            annotated = self.detector.draw_detections(
                image,
                detections,
                show_boxes=self.settings.get("show_boxes", True),
                show_labels=self.settings.get("show_labels", True),
                show_confidence=self.settings.get("show_confidence", True),
            )
            
            if self.settings.get("show_count", False):
                annotated = MediaHandler.add_count_overlay(annotated, detections)
            
            self.frame_processed.emit(annotated, detections)
            self.progress.emit(100)
            self.finished.emit([annotated])
        
        except Exception as e:
            self.error.emit(f"Image processing failed: {str(e)}")
    
    def _process_video(self):
        """Process video frames"""
        try:
            cap, metadata = MediaHandler.load_video(self.media_path)
            frames = []
            frame_count = 0
            frame_skip = self.settings.get("frame_skip", 1)
            
            while self.is_running:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                if frame_count % frame_skip == 0:
                    detections = self.detector.detect(frame)
                    annotated = self.detector.draw_detections(
                        frame,
                        detections,
                        show_boxes=self.settings.get("show_boxes", True),
                        show_labels=self.settings.get("show_labels", True),
                        show_confidence=self.settings.get("show_confidence", True),
                    )
                    
                    if self.settings.get("show_count", False):
                        annotated = MediaHandler.add_count_overlay(annotated, detections)
                    
                    frames.append(annotated)
                    self.frame_processed.emit(annotated, detections)
                else:
                    frames.append(frame)
                
                progress = int((frame_count / metadata["total_frames"]) * 100)
                self.progress.emit(progress)
            
            cap.release()
            self.finished.emit(frames)
        
        except Exception as e:
            self.error.emit(f"Video processing failed: {str(e)}")
    
    def stop(self):
        """Stop processing"""
        self.is_running = False
        self.wait()
