"""Main Application Window"""
import sys
import cv2
from pathlib import Path
from typing import Optional, List

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSlider, QCheckBox, QSpinBox, QFileDialog,
    QMessageBox, QProgressBar, QComboBox, QFrame, QScrollArea,
    QSizePolicy
)
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSlot

from src.config import (
    MODEL_CONFIG, UI_CONFIG, settings,
    OUTPUTS_DIR, MODEL_PATH
)
from src.core.detector import AerialDetector
from src.core.media_handler import MediaHandler
from src.utils.worker import ProcessingWorker


class SettingsPanel(QFrame):
    """Right sidebar settings panel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        self.init_ui()
    
    def init_ui(self):
        """Initialize settings UI"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title
        title = QLabel("⚙️ Detection Settings")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Confidence threshold
        layout.addWidget(QLabel("Confidence Threshold"))
        self.conf_slider = QSlider(Qt.Horizontal)
        self.conf_slider.setRange(0, 100)
        self.conf_slider.setValue(int(MODEL_CONFIG["confidence_threshold"] * 100))
        layout.addWidget(self.conf_slider)
        
        self.conf_label = QLabel(f"{MODEL_CONFIG['confidence_threshold']:.2f}")
        self.conf_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.conf_label)
        
        # IOU threshold
        layout.addWidget(QLabel("IOU Threshold"))
        self.iou_slider = QSlider(Qt.Horizontal)
        self.iou_slider.setRange(0, 100)
        self.iou_slider.setValue(int(MODEL_CONFIG["iou_threshold"] * 100))
        layout.addWidget(self.iou_slider)
        
        self.iou_label = QLabel(f"{MODEL_CONFIG['iou_threshold']:.2f}")
        self.iou_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.iou_label)
        
        layout.addWidget(QLabel(""))  # Spacer
        
        # Visualization options
        viz_title = QLabel("🎨 Visualization")
        viz_title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(viz_title)
        
        self.show_boxes = QCheckBox("Show Bounding Boxes")
        self.show_boxes.setChecked(settings.get("show_boxes", True))
        layout.addWidget(self.show_boxes)
        
        self.show_labels = QCheckBox("Show Class Labels")
        self.show_labels.setChecked(settings.get("show_labels", True))
        layout.addWidget(self.show_labels)
        
        self.show_confidence = QCheckBox("Show Confidence")
        self.show_confidence.setChecked(settings.get("show_confidence", True))
        layout.addWidget(self.show_confidence)
        
        self.show_count = QCheckBox("Show Count Overlay")
        self.show_count.setChecked(settings.get("show_count", False))
        layout.addWidget(self.show_count)
        
        self.side_by_side = QCheckBox("Side-by-Side View")
        self.side_by_side.setChecked(settings.get("side_by_side", True))
        layout.addWidget(self.side_by_side)
        
        layout.addWidget(QLabel(""))  # Spacer
        
        # Video options
        video_title = QLabel("🎬 Video Options")
        video_title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(video_title)
        
        layout.addWidget(QLabel("Frame Skip"))
        self.frame_skip = QSpinBox()
        self.frame_skip.setRange(1, 30)
        self.frame_skip.setValue(settings.get("frame_skip", 1))
        layout.addWidget(self.frame_skip)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def get_settings(self) -> dict:
        """Get all settings as dict"""
        return {
            "confidence": self.conf_slider.value() / 100.0,
            "iou": self.iou_slider.value() / 100.0,
            "show_boxes": self.show_boxes.isChecked(),
            "show_labels": self.show_labels.isChecked(),
            "show_confidence": self.show_confidence.isChecked(),
            "show_count": self.show_count.isChecked(),
            "side_by_side": self.side_by_side.isChecked(),
            "frame_skip": self.frame_skip.value(),
        }


class PreviewArea(QFrame):
    """Central preview area for images/videos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("border: 2px solid #333; border-radius: 8px; background-color: #1a1a1a;")
        self.setMinimumSize(800, 600)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 400)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.image_label)
        
        # Info label
        self.info_label = QLabel("📁 Load an image or video to start detection")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
    
    def set_image(self, cv_image):
        """Display OpenCV image"""
        h, w = cv_image.shape[:2]
        
        # Resize if too large
        max_w, max_h = 900, 650
        if w > max_w or h > max_h:
            scale = min(max_w / w, max_h / h)
            w, h = int(w * scale), int(h * scale)
            cv_image = cv2.resize(cv_image, (w, h))
        
        # Convert
        cv_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        h, w, ch = cv_rgb.shape
        bytes_per_line = 3 * w
        qt_image = QImage(cv_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        self.image_label.setPixmap(pixmap)
    
    def set_info(self, text: str, status: str = "info"):
        """Set info label"""
        colors = {
            "info": "#888",
            "success": "#0f0",
            "error": "#f00",
            "processing": "#0ff",
        }
        color = colors.get(status, colors["info"])
        self.info_label.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
        self.info_label.setText(text)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize detector
        try:
            if not MODEL_PATH.exists():
                raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
            self.detector = AerialDetector(MODEL_PATH)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model:\n{str(e)}")
            sys.exit(1)
        
        # Initialize worker
        self.worker = ProcessingWorker(self.detector)
        self.worker.frame_processed.connect(self.on_frame_processed)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.progress.connect(self.on_progress)
        self.worker.error.connect(self.on_error)
        
        # State
        self.current_frames: List = []
        self.current_detections: List = []
        self.current_media_path: Optional[Path] = None
        self.is_processing = False
        
        # Setup UI
        self.setWindowTitle("🦅 Aerial Person Detection")
        self.setGeometry(100, 50, UI_CONFIG["window_width"], UI_CONFIG["window_height"])
        self.init_ui()
        
        # Load settings
        self.load_settings()
    
    def init_ui(self):
        """Initialize main UI"""
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left: Control panel
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        
        # File input section
        file_frame = QFrame()
        file_frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        file_layout = QVBoxLayout()
        
        title = QLabel("📁 Input")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        file_layout.addWidget(title)
        
        self.open_image_btn = QPushButton("📷 Open Image")
        self.open_image_btn.clicked.connect(self.open_image)
        file_layout.addWidget(self.open_image_btn)
        
        self.open_video_btn = QPushButton("🎬 Open Video")
        self.open_video_btn.clicked.connect(self.open_video)
        file_layout.addWidget(self.open_video_btn)
        
        self.webcam_btn = QPushButton("📹 Use Webcam")
        self.webcam_btn.clicked.connect(self.use_webcam)
        file_layout.addWidget(self.webcam_btn)
        
        file_frame.setLayout(file_layout)
        left_layout.addWidget(file_frame)
        
        # Processing section
        proc_frame = QFrame()
        proc_frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        proc_layout = QVBoxLayout()
        
        proc_title = QLabel("⚡ Processing")
        proc_title.setFont(QFont("Arial", 12, QFont.Bold))
        proc_layout.addWidget(proc_title)
        
        self.process_btn = QPushButton("🚀 Run Detection")
        self.process_btn.clicked.connect(self.run_detection)
        self.process_btn.setEnabled(False)
        proc_layout.addWidget(self.process_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        proc_layout.addWidget(self.stop_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        proc_layout.addWidget(self.progress_bar)
        
        proc_frame.setLayout(proc_layout)
        left_layout.addWidget(proc_frame)
        
        # Output section
        output_frame = QFrame()
        output_frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        output_layout = QVBoxLayout()
        
        output_title = QLabel("💾 Output")
        output_title.setFont(QFont("Arial", 12, QFont.Bold))
        output_layout.addWidget(output_title)
        
        self.save_image_btn = QPushButton("💾 Save Image")
        self.save_image_btn.clicked.connect(self.save_image)
        self.save_image_btn.setEnabled(False)
        output_layout.addWidget(self.save_image_btn)
        
        self.save_video_btn = QPushButton("💾 Save Video")
        self.save_video_btn.clicked.connect(self.save_video)
        self.save_video_btn.setEnabled(False)
        output_layout.addWidget(self.save_video_btn)
        
        self.open_output_btn = QPushButton("📂 Open Outputs Folder")
        self.open_output_btn.clicked.connect(self.open_outputs_folder)
        output_layout.addWidget(self.open_output_btn)
        
        output_frame.setLayout(output_layout)
        left_layout.addWidget(output_frame)
        
        # Stats section
        stats_frame = QFrame()
        stats_frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        stats_layout = QVBoxLayout()
        
        stats_title = QLabel("📊 Statistics")
        stats_title.setFont(QFont("Arial", 12, QFont.Bold))
        stats_layout.addWidget(stats_title)
        
        self.count_label = QLabel("Objects: 0")
        self.count_label.setFont(QFont("Arial", 10))
        stats_layout.addWidget(self.count_label)
        
        self.class_label = QLabel("Person: 0")
        self.class_label.setFont(QFont("Arial", 10))
        stats_layout.addWidget(self.class_label)
        
        stats_frame.setLayout(stats_layout)
        left_layout.addWidget(stats_frame)
        
        left_layout.addStretch()
        
        # Center: Preview
        center_layout = QVBoxLayout()
        self.preview = PreviewArea()
        center_layout.addWidget(self.preview)
        
        # Right: Settings
        right_layout = QVBoxLayout()
        self.settings_panel = SettingsPanel()
        scroll = QScrollArea()
        scroll.setWidget(self.settings_panel)
        scroll.setWidgetResizable(True)
        right_layout.addWidget(scroll)
        
        # Combine layouts
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(250)
        
        center_widget = QWidget()
        center_widget.setLayout(center_layout)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_widget.setMaximumWidth(280)
        
        main_layout.addWidget(left_widget, 0)
        main_layout.addWidget(center_widget, 1)
        main_layout.addWidget(right_widget, 0)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Apply dark theme
        self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Apply dark theme stylesheet"""
        dark_style = """
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #fff;
            }
            QLabel {
                color: #fff;
            }
            QPushButton {
                background-color: #0d47a1;
                color: #fff;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0a3d91;
            }
            QPushButton:disabled {
                background-color: #444;
                color: #888;
            }
            QSlider::groove:horizontal {
                background-color: #444;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #0d47a1;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QCheckBox {
                color: #fff;
                spacing: 5px;
            }
            QSpinBox {
                background-color: #333;
                color: #fff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #333;
                text-align: center;
                color: #fff;
            }
            QProgressBar::chunk {
                background-color: #0d47a1;
            }
            QFrame {
                background-color: #2a2a2a;
            }
            QScrollArea {
                background-color: #1e1e1e;
            }
        """
        self.setStyleSheet(dark_style)
    
    def open_image(self):
        """Open image file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "",
            "Images (*.jpg *.jpeg *.png *.bmp *.tiff)"
        )
        
        if file_path:
            self.current_media_path = Path(file_path)
            try:
                image = MediaHandler.load_image(self.current_media_path)
                self.preview.set_image(image)
                self.preview.set_info(f"✓ Loaded: {self.current_media_path.name}", "success")
                self.process_btn.setEnabled(True)
            except Exception as e:
                self.preview.set_info(f"✗ Error: {str(e)}", "error")
    
    def open_video(self):
        """Open video file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Video", "",
            "Videos (*.mp4 *.avi *.mov *.mkv *.flv)"
        )
        
        if file_path:
            self.current_media_path = Path(file_path)
            try:
                cap, _ = MediaHandler.load_video(self.current_media_path)
                ret, frame = cap.read()
                cap.release()
                
                if ret:
                    self.preview.set_image(frame)
                    self.preview.set_info(f"✓ Loaded: {self.current_media_path.name}", "success")
                    self.process_btn.setEnabled(True)
            except Exception as e:
                self.preview.set_info(f"✗ Error: {str(e)}", "error")
    
    def use_webcam(self):
        """Use webcam"""
        QMessageBox.info(self, "Webcam", "Webcam support coming soon!")
    
    def run_detection(self):
        """Run detection on selected media"""
        if not self.current_media_path:
            QMessageBox.warning(self, "Error", "Please select an image or video first")
            return
        
        # Get settings
        settings_dict = self.settings_panel.get_settings()
        
        # Update detector thresholds
        self.detector.set_thresholds(settings_dict["confidence"], settings_dict["iou"])
        
        # Disable buttons
        self.is_processing = True
        self.process_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        
        # Determine if video or image
        is_video = self.current_media_path.suffix.lower() in {".mp4", ".avi", ".mov", ".mkv", ".flv"}
        
        # Start worker
        self.worker.set_media(self.current_media_path, is_video)
        self.worker.set_settings(
            show_boxes=settings_dict["show_boxes"],
            show_labels=settings_dict["show_labels"],
            show_confidence=settings_dict["show_confidence"],
            show_count=settings_dict["show_count"],
            frame_skip=settings_dict["frame_skip"],
        )
        self.worker.start()
        
        self.preview.set_info("Processing...", "processing")
    
    def stop_processing(self):
        """Stop detection"""
        self.worker.stop()
        self.is_processing = False
        self.process_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.preview.set_info("Processing stopped", "info")
    
    @pyqtSlot(object, list)
    def on_frame_processed(self, frame, detections):
        """Handle processed frame"""
        self.current_frames.append(frame)
        self.current_detections.append(detections)
        
        # Display latest frame
        self.preview.set_image(frame)
        
        # Update stats
        total = sum(len(d) for d in self.current_detections)
        self.count_label.setText(f"Objects: {total}")
        self.class_label.setText(f"Person: {total}")
    
    @pyqtSlot(list)
    def on_processing_finished(self, frames):
        """Handle processing completion"""
        self.current_frames = frames
        self.is_processing = False
        self.process_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        self.save_image_btn.setEnabled(True)
        self.save_video_btn.setEnabled(True)
        
        total = sum(len(d) for d in self.current_detections)
        self.preview.set_info(f"✓ Complete! Detected {total} objects", "success")
    
    @pyqtSlot(int)
    def on_progress(self, value):
        """Handle progress update"""
        self.progress_bar.setValue(value)
    
    @pyqtSlot(str)
    def on_error(self, error_msg):
        """Handle processing error"""
        self.is_processing = False
        self.process_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.preview.set_info(f"✗ Error: {error_msg}", "error")
        QMessageBox.critical(self, "Processing Error", error_msg)
    
    def save_image(self):
        """Save annotated image"""
        if not self.current_frames:
            QMessageBox.warning(self, "Error", "No processed image to save")
            return
        
        output_path = OUTPUTS_DIR / f"{self.current_media_path.stem}_detected.png"
        try:
            MediaHandler.save_image(self.current_frames[-1], output_path)
            QMessageBox.information(self, "Success", f"Image saved:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def save_video(self):
        """Save annotated video"""
        if not self.current_frames:
            QMessageBox.warning(self, "Error", "No processed video to save")
            return
        
        output_path = OUTPUTS_DIR / f"{self.current_media_path.stem}_detected.mp4"
        try:
            MediaHandler.save_video(self.current_frames, output_path)
            QMessageBox.information(self, "Success", f"Video saved:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def open_outputs_folder(self):
        """Open outputs folder in explorer"""
        import os
        import subprocess
        
        if not OUTPUTS_DIR.exists():
            OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        
        if sys.platform == "win32":
            os.startfile(str(OUTPUTS_DIR))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(OUTPUTS_DIR)])
        else:
            subprocess.Popen(["xdg-open", str(OUTPUTS_DIR)])
    
    def load_settings(self):
        """Load saved settings"""
        self.settings_panel.conf_slider.setValue(int(settings.get("confidence_threshold", 0.5) * 100))
        self.settings_panel.iou_slider.setValue(int(settings.get("iou_threshold", 0.45) * 100))
        self.settings_panel.show_boxes.setChecked(settings.get("show_boxes", True))
        self.settings_panel.show_labels.setChecked(settings.get("show_labels", True))
        self.settings_panel.show_confidence.setChecked(settings.get("show_confidence", True))
        self.settings_panel.show_count.setChecked(settings.get("show_count", False))
        self.settings_panel.side_by_side.setChecked(settings.get("side_by_side", True))
        self.settings_panel.frame_skip.setValue(settings.get("frame_skip", 1))
    
    def closeEvent(self, event):
        """Save settings on close"""
        settings_dict = self.settings_panel.get_settings()
        settings.update(**settings_dict)
        
        self.worker.stop()
        event.accept()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
