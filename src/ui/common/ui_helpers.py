from PyQt6.QtWidgets import QLineEdit, QComboBox, QDateEdit
from PyQt6.QtCore import QDate
from .enums import FieldType

class WidgetFactory:
    @staticmethod
    def create_widget(field_type, value=None):
        """
        Factory that creates and populates a widget based on FieldType.
        Returns: The configured widget (QComboBox, QDateEdit, or QLineEdit).
        """
        
        # --- 1. COMBOBOX ---
        if field_type == FieldType.SEX_COMBOBOX:
            widget = QComboBox()
            widget.addItems(["", "M", "F"])
            if value:
                widget.setCurrentText(str(value).strip())
            return widget

        # --- 2. DATE EDIT ---
        elif field_type == FieldType.DATE:
            widget = QDateEdit()
            widget.setDisplayFormat("yyyy-MM-dd")
            widget.setCalendarPopup(True)
            
            # -- data handling --
            if not value:
                # Case 1: Value is Empty/None -> Default to Today
                widget.setDate(QDate.currentDate())
            
            elif isinstance(value, str):
                # Case 2: It's a String (e.g. from SQLite) -> Parse it
                qdate = QDate.fromString(value, "yyyy-MM-dd")
                if qdate.isValid():
                    widget.setDate(qdate)
                else:
                    # String was garbage? Default to Today
                    widget.setDate(QDate.currentDate())

            else:
                # Case 3: It's a Python Date/Datetime Object (e.g. from Postgres)
                try:
                    widget.setDate(QDate(value.year, value.month, value.day))
                except AttributeError:
                    # Case 4: It's some unknown type -> Default to Today to prevent crash
                    print(f"Warning: Could not convert {type(value)} to QDate")
                    widget.setDate(QDate.currentDate())
            return widget
        
        # --- 3. TEXT ---
        else:
            widget = QLineEdit()
            if value:
                widget.setText(str(value))
            return widget

    @staticmethod
    def extract_value(obj):
        if obj is None:
            return ""
        if isinstance(obj, QComboBox):
            return obj.currentText()
        if isinstance(obj, QDateEdit):
            return obj.date().toString("yyyy-MM-dd")
        #  Handle Standard Items (QLineEdit, QTableWidgetItem, etc.)
        if hasattr(obj, 'text'):
            return obj.text().strip()
            
        #  Final Fallback: If it's not None, but not a known text type
        return ""
        
