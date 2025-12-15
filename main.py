import sys
import os

# Ensure Python can see the 'src' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show the window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())