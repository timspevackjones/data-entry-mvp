import csv
import os


class DataManager:
    def __init__(self, filename="data.csv"):
        self.filename = filename

    def save_data(self, patient_id, patient_name):
        file_exists = os.path.exists(self.filename)

        with open(self.filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Patient ID", "Patient Name"])
            writer.writerow([patient_id, patient_name])

        print(
            "Data saved:",
            f"ID={patient_id}, Name={patient_name}, saved to {self.filename}",
        )
