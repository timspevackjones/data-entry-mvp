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
                # Optional: Debug print
                # print(f"DEBUG: Row {row_idx} changed.")

                try:
                    # Map columns by name
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
