from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QMenu,
    QGridLayout,
    QMessageBox,
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from data_manager import DataManager

import sys


class PlaceholderInput(QLineEdit):
    def __init__(self, placeholder_text):
        # 1. Initialize the parent QLineEdit
        super().__init__()
        # 2. Set the custom property immediately
        self.setPlaceholderText(placeholder_text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Entry MVP")

        self.data_manager = DataManager("MVP_data_entry.csv")

        label_patient_id = QLabel("Patient ID")
        self.input_patient_id = PlaceholderInput("Enter Patient ID")

        label_patient_name = QLabel("Patient name")
        self.input_patient_name = PlaceholderInput("Enter Patient Name")

        button = QPushButton("Submit data")

        layout1 = QVBoxLayout()
        layout2 = QGridLayout()
        layout2.setVerticalSpacing(5)
        layout2.setHorizontalSpacing(15)

        layout2.addWidget((label_patient_id), 0, 0)
        layout2.addWidget((self.input_patient_id), 1, 0)

        layout2.addWidget((label_patient_name), 0, 1)
        layout2.addWidget((self.input_patient_name), 1, 1)

        layout1.addLayout(layout2)
        layout1.addSpacing(20)
        layout1.addWidget(button)

        # pushes everything to the top
        layout1.addStretch()

        # set margins around the layout
        layout1.setContentsMargins(20, 20, 20, 20)

        container = QWidget()
        container.setLayout(layout1)

        button.clicked.connect(self.send_data)

        # set up for right click context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # Set fixed size for the window.
        self.setFixedSize(QSize(400, 300))

        self.setCentralWidget(container)

    def send_data(self):

        p_id = self.input_patient_id.text().strip()
        p_name = self.input_patient_name.text().strip()

        if not p_id:
            QMessageBox.warning(self, "Validation Error", "Patient ID is missing.")
            return
        if not p_name:
            QMessageBox.warning(self, "Validation Error", "Patient Name is missing.")
            return

        try:
            self.data_manager.save_data(p_id, p_name)
            QMessageBox.information(self, "Success", "Data saved successfully!")

            # --- CLEAR FORM FOR NEXT ENTRY ---
            self.input_patient_id.clear()
            self.input_patient_name.clear()

        except Exception as e:
            print(f"Crashed while saving ID: {p_id} Name: {p_name}")
            print(f"Error saving data: {e}")
            QMessageBox.critical(self, "System Error", f"Could not save data:\n{e}")

    def on_context_menu(self, pos):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(self.mapToGlobal(pos))


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
