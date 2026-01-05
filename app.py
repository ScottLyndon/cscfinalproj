"""Application Entry Point"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

from src.ui.main_window import MainWindow
from src.config import MODEL_PATH


def main():
    """Launch application"""
    # Check model exists
    if not MODEL_PATH.exists():
        print(f"Error: Model not found at {MODEL_PATH}")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
