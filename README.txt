Data Entry MVP
Version: 1.0
Developer: Tim Jones

OVERVIEW:
This application is an offline data entry tool designed to replace MS Access forms.
It accepts user input, validates it, and saves it to a local CSV file.

CONTENTS:
1. /Runnable_Demo
   Contains a zipped version of the compiled application and a single executable
   - Instructions: 
     1. Copy the zip file to your desktop.
     2. Right-click -> Extract All.
     3. Open the folder and double-click "UCL_Data_Entry_MVP.exe".

2. /Source_Code: The full Python source code for security audit.
   - Built using: Python 3.13, PyQt6.
   - Setup Instructions:
     1. pip install -r requirements.txt
   - Build instructions
     Option A - Recommended:
     Run the included spec file to generate the exact build configuration used in the demo:
     pyinstaller UCL_Data_Entry_MVP.spec
     Option B - Manual:
     pyinstaller --onedir --noconsole --name="UCL_Data_Entry_MVP" main.py

3. /Developer_Guide
   How to adapt this MVP for a different Database Table:

   A. Database Configuration (DataManager.py):
      1. Open DataManager.py.
      2. Locate the __init__ method.
      3. Update 'self.table_name' to your SQL table name (e.g., "tblEmployees").
      4. Update 'self.primary_key_col' to your primary key column (e.g., "EmployeeID").
      5. Update 'self.db_sort_order' to control how records appear.
         - Set to None to default to the Primary Key (e.g., self.db_sort_order = None).
         - Set to a string for custom sorting (e.g., self.db_sort_order = "Surname, FirstName").
      6. Update 'self.ignored_columns' to exclude any columns that should not be edited (e.g., auto-calculated dates).

   B. UI Configuration (schema.py):
      1. Open schema.py.
      2. Update 'COLUMN_MAP' to match your database columns exactly.
      3. Assign a FieldType (TEXT, DATE, READONLY) to control how the column appears in the UI.
      4. New FieldTypes can be managed within enums.py.

   C. Connection String (.env):
      1. Ensure your .env file contains the correct SQL_CONNECTION_STRING for the new database.

ADDITIONAL NOTES:
- This application is 100% offline. It makes no network requests.
- Data is saved locally to "MVP_data_entry.csv" in the same folder as the app.