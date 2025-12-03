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
     pyinstaller --onedir --noconsole --name="UCL_Data_Entry_MVP" app.py

ADDITIONAL NOTES:
- This application is 100% offline. It makes no network requests.
- Data is saved locally to "MVP_data_entry.csv" in the same folder as the app.