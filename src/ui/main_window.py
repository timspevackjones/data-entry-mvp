from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QDateEdit,
)
from datetime import date, datetime
from PyQt6.QtCore import QDate, Qt
from src.database.data_manager import DataManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UCL Data Haven - Table View")
        self.resize(1000, 600)  # Make it wide like Excel

        self.data_manager = DataManager()

        # 1. Store Data & Headers
        self.headers = []
        self.current_data = []

        # 2. Setup the UI
        self.setup_ui()

        # 3. Load Data & Fill Table
        self.refresh_data()

    def setup_ui(self):
        # Main Layout
        layout = QVBoxLayout()

        # --- THE TABLE ---
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # --- REFRESH BUTTON (To reload from DB) ---
        self.btn_refresh = QPushButton("Refresh / Discard Changes")
        self.btn_refresh.clicked.connect(self.refresh_data)
        layout.addWidget(self.btn_refresh)

        # --- SAVE BUTTON (Iterates table to save changes) ---
        # Note: We will implement the actual 'Save' logic in the next step
        self.btn_save = QPushButton("Save Changes to Database")
        self.btn_save.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold;"
        )
        self.btn_save.clicked.connect(self.save_data)
        layout.addWidget(self.btn_save)

        # Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def refresh_data(self):
        """Fetches data from SQL and rebuilds the table"""
        # 1. Get Data
        self.headers, self.current_data = self.data_manager.get_all_records()

        # 2. Configure Table Dimensions
        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(len(self.current_data))
        self.table.setHorizontalHeaderLabels(self.headers)

        # 3. Populate Rows
        self.populate_table()

    def populate_table(self):
        # Turn off signals while building to prevent lag
        self.table.setSortingEnabled(False)

        # The Rule Book
        special_rules = {
            "RecID": "READONLY",
            "StatusDate": "READONLY",
            "Sex": "SEX_COMBOBOX",
            "DateOfBirth": "DATE",
            "Status": "READONLY",
        }

        # Loop through every row of data
        for row_idx, row_data in enumerate(self.current_data):

            # Loop through every column in that row
            for col_idx, col_name in enumerate(self.headers):
                cell_value = row_data[col_idx]
                rule = special_rules.get(col_name, "TEXT")

                # --- LOGIC TO CHOOSE CELL TYPE ---

                if rule == "READONLY":
                    # Standard Item, but grayed out and locked
                    item = QTableWidgetItem(str(cell_value))
                    item.setFlags(
                        item.flags() ^ Qt.ItemFlag.ItemIsEditable
                    )  # Remove edit flag
                    item.setBackground(Qt.GlobalColor.lightGray)
                    self.table.setItem(row_idx, col_idx, item)

                elif rule == "SEX_COMBOBOX":
                    # Create a dropdown
                    combo = QComboBox()
                    combo.addItems(["", "M", "F"])
                    combo.setCurrentText(str(cell_value).strip() if cell_value else "")
                    # Embed it into the table cell
                    self.table.setCellWidget(row_idx, col_idx, combo)

                elif rule == "DATE":
                    # Create a date picker
                    date_edit = QDateEdit()
                    date_edit.setDisplayFormat("yyyy-MM-dd")
                    date_edit.setCalendarPopup(True)

                    if cell_value:
                        qdate = QDate(cell_value.year, cell_value.month, cell_value.day)
                        date_edit.setDate(qdate)
                    else:
                        date_edit.setDate(QDate.currentDate())

                    # Embed it
                    self.table.setCellWidget(row_idx, col_idx, date_edit)

                else:
                    # Standard Text Cell
                    # Convert None to empty string
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

    def save_data(self):
        changes_count = 0
        errors = []

        # Loop through every row in the UI
        for row_idx in range(self.table.rowCount()):

            # 1. Get the Current UI Data
            new_data = self.get_table_row_data(row_idx)

            # 2. Get the Original Data (Snapshot)
            # Note: self.current_data is a list of tuples/lists.
            # We need to make sure we compare strings to strings.
            original_row = self.current_data[row_idx]

            # Convert original to string list for fair comparison
            # (Because SQL gives us Objects like datetime.date, but UI gives us Strings)
            original_strings = []
            for val in original_row:
                if val is None:
                    original_strings.append("")
                elif isinstance(val, datetime):
                    # Keep the time for StatusDate!
                    original_strings.append(str(val))
                elif isinstance(val, date):
                    original_strings.append(val.strftime("%Y-%m-%d"))
                else:
                    original_strings.append(str(val).strip())

            # 3. COMPARE: Did anything change?
            if new_data != original_strings:
                for i, (new_val, old_val) in enumerate(zip(new_data, original_strings)):
                    if new_val != old_val:
                        col_name = self.headers[i]
                        print(
                            f"DEBUG: Row {row_idx} change detected in '{col_name}': "
                            f"'{new_val}' vs '{old_val}'"
                        )

                try:
                    rec_id = new_data[self.headers.index("RecID")]
                    family = new_data[self.headers.index("FamilySerial")]
                    member_id = new_data[self.headers.index("CohortMemberID")]
                    surname = new_data[self.headers.index("Surname")]
                    first = new_data[self.headers.index("FirstName")]
                    title = new_data[self.headers.index("Title")]
                    sex = new_data[self.headers.index("Sex")]
                    dob = new_data[self.headers.index("DateOfBirth")]
                    status = new_data[self.headers.index("Status")]

                    # Send to DB
                    success, msg = self.data_manager.update_record(
                        rec_id,
                        family,
                        member_id,
                        surname,
                        first,
                        title,
                        sex,
                        dob,
                        status,
                    )

                    if success:
                        changes_count += 1
                    else:
                        errors.append(f"Row {row_idx}: {msg}")

                except ValueError as e:
                    print(f"Skipping row {row_idx} due to missing column: {e}")

        # 4. Final Report
        if errors:
            QMessageBox.warning(self, "Warnings", "\n".join(errors))

        if changes_count > 0:
            QMessageBox.information(
                self, "Saved", f"Successfully updated {changes_count} records."
            )
            self.refresh_data()  # Reload from DB to get fresh Snapshot
        else:
            QMessageBox.information(
                self, "No Changes", "No modifications were detected."
            )
