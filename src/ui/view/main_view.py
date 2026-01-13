from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit
)
from PyQt6.QtCore import QDate, Qt
from src.ui.common.enums import FieldType
from src.ui.common.schema import COLUMN_MAP, SEARCH_FIELDS




class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UCL Data Haven - Table View")
        self.resize(1000, 600)  # Make it wide like Excel

        # 1. Store Data & Headers
        self.headers = []
        self.current_data = []

        # 2. Setup the UI
        self.setup_ui()

    def setup_ui(self):
        # Main Layout
        layout = QVBoxLayout()

        # -- SETUP SEARCH BAR ---
        self.setup_search_bar()
        layout.addWidget(self.search_group)

        # --- THE TABLE ---
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # --- REFRESH BUTTON (To reload from DB) ---
        self.btn_refresh = QPushButton("Refresh / Discard Changes")
        layout.addWidget(self.btn_refresh)

        # --- SAVE BUTTON (Iterates table to save changes) ---
        self.btn_save = QPushButton("Save Changes to Database")
        self.btn_save.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold;"
        )
        layout.addWidget(self.btn_save)

        # Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def setup_search_bar(self):
        """Creates the search input fields above the table."""
        self.search_group = QGroupBox("Search Filters")
        self.search_layout = QHBoxLayout()
      
        self.search_inputs = {}

        for field in SEARCH_FIELDS:
            # Create a label and input for each
            label = QLabel(field + ":")
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Search {field}...")
            
            # Add to layout
            self.search_layout.addWidget(label)
            self.search_layout.addWidget(line_edit)
            
            # Store reference so we can read it later
            self.search_inputs[field] = line_edit

        # Add Search Button
        self.btn_search = QPushButton("Search")
        self.btn_search.setFixedWidth(100)
        self.search_layout.addWidget(self.btn_search)

        # Add Clear Button
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setFixedWidth(80)
        self.search_layout.addWidget(self.btn_clear)

        self.search_group.setLayout(self.search_layout)  

    def get_search_params(self):
        """Returns a dictionary of filled-out search fields."""
        search_data = {}
        for field, widget in self.search_inputs.items():
            text = widget.text().strip()
            if text:
                search_data[field] = text
        return search_data

    def clear_search_fields(self):
        """Clears all text boxes."""
        for widget in self.search_inputs.values():
            widget.clear()

    def set_table_data(self, headers, data):
        """Called by Presenter to display data"""
        self.headers = headers
        self.current_data = data

        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(len(self.current_data))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.populate_table()

    def populate_table(self):
        # Turn off signals while building to prevent lag
        self.table.setSortingEnabled(False)

        # Loop through every row of data
        for row_idx, row_data in enumerate(self.current_data):

            # Loop through every column in that row
            for col_idx, col_name in enumerate(self.headers):
                cell_value = row_data[col_idx]

                # If the column isn't in the map, default to FieldType.TEXT
                field_type = COLUMN_MAP.get(col_name, FieldType.TEXT)

                # --- LOGIC TO CHOOSE CELL TYPE ---

                if field_type == FieldType.READONLY:
                    # Standard Item, but grayed out and locked
                    item = QTableWidgetItem(str(cell_value))
                    item.setFlags(
                        item.flags() ^ Qt.ItemFlag.ItemIsEditable
                    )  # Remove edit flag
                    item.setBackground(Qt.GlobalColor.lightGray)
                    self.table.setItem(row_idx, col_idx, item)

                elif field_type == FieldType.SEX_COMBOBOX:
                    # Create a dropdown
                    combo = QComboBox()
                    combo.addItems(["", "M", "F"])
                    combo.setCurrentText(str(cell_value).strip() if cell_value else "")
                    # Embed it into the table cell
                    self.table.setCellWidget(row_idx, col_idx, combo)

                elif field_type == FieldType.DATE:
                    # Create a date picker
                    date_edit = QDateEdit()
                    date_edit.setDisplayFormat("yyyy-MM-dd")
                    date_edit.setCalendarPopup(True)

                    if cell_value:
                        # Safety check: ensure cell_value is actually a date object
                        # (sometimes SQL returns strings depending on the driver)
                        try:
                            qdate = QDate(cell_value.year, cell_value.month, cell_value.day)
                            date_edit.setDate(qdate)
                        except AttributeError:
                             # Fallback if it came through as a string
                            date_edit.setDate(QDate.currentDate())
                    else:
                        date_edit.setDate(QDate.currentDate())

                    # Embed it
                    self.table.setCellWidget(row_idx, col_idx, date_edit)

                else:
                    # Default: FieldType.TEXT
                    display_text = str(cell_value) if cell_value is not None else ""
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(display_text))

        # Make it look nice
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def get_table_row_data(self, row_idx):
        """
        Helper to extract clean data from a single row of widgets.
        Returns a list of values: ['1', 'A111', 'Hall', ...]
        """
        row_values = []
        for col_idx, col_name in enumerate(self.headers):
            # Check if there is a special widget (Combo/Date)
            widget = self.table.cellWidget(row_idx, col_idx)
            item = self.table.item(row_idx, col_idx)
            if widget:
                # Extraction logic for special widgets
                if isinstance(widget, QComboBox):
                    row_values.append(widget.currentText())
                elif isinstance(widget, QDateEdit):
                    row_values.append(widget.date().toString("yyyy-MM-dd"))
            else:
                # Extraction logic for standard text cells
                # If item is None (empty), return ""
                row_values.append(item.text().strip() if item else "")

        return row_values

    def get_all_data(self):
        """Returns a list of lists containing all table data as strings"""
        all_data = []
        for row_idx in range(self.table.rowCount()):
            all_data.append(self.get_table_row_data(row_idx))
        return all_data
