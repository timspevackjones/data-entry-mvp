from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QDialogButtonBox, QComboBox, QDateEdit, QMessageBox
)
from PyQt6.QtCore import QDate
from ..common.schema import COLUMN_MAP, INSERT_FIELDS
from ..common.enums import FieldType
from ..common.ui_helpers import WidgetFactory

class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Record")
        self.resize(400, 500)
        
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        
        # Dictionary to hold the input widgets so we can read them later
        self.inputs = {}

        # --- DYNAMICALLY BUILD FORM ---
        for field in INSERT_FIELDS:
            field_type = COLUMN_MAP.get(field, FieldType.TEXT)
            
            widget = WidgetFactory.create_widget(field_type, value=None)
            
            self.form_layout.addRow(f"{field}:", widget)
            self.inputs[field] = widget

        self.layout.addLayout(self.form_layout)

        # --- BUTTONS (OK / CANCEL) ---
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_data(self):
        """Extracts data from the widgets into a dictionary."""
        data = {}
        for field, widget in self.inputs.items():
        
            # Only include if not empty (SQL handles NULLs better if we just omit empty strings, 
            # or you can send '' depending on your DB preference. 
            # For now, we send everything.)
            data[field] = WidgetFactory.extract_value(widget)
        return data
    
