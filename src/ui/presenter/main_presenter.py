from PyQt6.QtWidgets import QMessageBox
from datetime import date, datetime


class MainPresenter:
    def __init__(self, view, data_manager):
        self.view = view
        self.data_manager = data_manager

        # Internal storage for snapshot comparison
        self.headers = []
        self.original_data = []

        # Connect to View signals
        self.view.btn_refresh.clicked.connect(self.load_data)
        self.view.btn_save.clicked.connect(self.handle_save)

        # Initial Load
        self.load_data()

    def load_data(self):
        """Fetches data from Model and updates View"""
        self.headers, self.original_data = self.data_manager.get_all_records()
        self.view.set_table_data(self.headers, self.original_data)

    def handle_save(self):
        """Orchestrates the save logic: View -> Compare -> Model"""
        changes_count = 0
        errors = []

        # 1. Get the Current UI Data from View
        all_rows_ui_data = self.view.get_all_data()

        # Loop through every row
        for row_idx, new_data in enumerate(all_rows_ui_data):

            # 2. Get the Original Data (Snapshot)
            if row_idx >= len(self.original_data):
                break  # Safety check

            original_row = self.original_data[row_idx]

            # Convert original to string list for fair comparison
            original_strings = []
            for val in original_row:
                if val is None:
                    original_strings.append("")
                elif isinstance(val, datetime):
                    original_strings.append(str(val))
                elif isinstance(val, date):
                    original_strings.append(val.strftime("%Y-%m-%d"))
                else:
                    original_strings.append(str(val).strip())

            # 3. COMPARE: Did anything change?
            if new_data != original_strings:

                # Instead of manually finding indexes for every single column,
                # the list is turned into a dictionary.
                # headers: ['RecID', 'Surname', 'FirstName', ...]
                # new_data: ['101', 'Smith', 'John', ...]
                # Result: {'RecID': '101', 'Surname': 'Smith', ...}

                # Optional: Debug print
                # print(f"DEBUG: Row {row_idx} changed.")

                # zip automatically pairs headers with new_data
                row_dict = dict(zip(self.headers, new_data))

                success, msg = self.data_manager.update_record(row_dict)

                if success:
                    changes_count += 1
                else:
                    print(f"DEBUG SQL ERROR: {msg}")
                    errors.append(f"Row {row_idx + 1}: Failed to save. Please check your data.")


        # 4. Final Report
        if errors:
            QMessageBox.warning(self.view, "Warnings", "\n".join(errors))

        if changes_count > 0:
            QMessageBox.information(
                self.view, "Saved", f"Successfully updated {changes_count} records."
            )
            self.load_data()  # Reload from DB to get fresh Snapshot
        else:
            QMessageBox.information(
                self.view, "No Changes", "No modifications were detected."
            )
