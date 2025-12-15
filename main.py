import sys
import os
from PyQt6.QtWidgets import QApplication
from src.ui.main_view import MainView
from src.ui.main_presenter import MainPresenter
from src.database.data_manager import DataManager

# Ensure Python can see the 'src' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Create the Model (Data)
    data_manager = DataManager()

    # 2. Create the View (UI)
    view = MainView()

    # 3. Create the Presenter (Logic) - wires them together
    presenter = MainPresenter(view, data_manager)

    view.show()

    # Start the event loop
    sys.exit(app.exec())
