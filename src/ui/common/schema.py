from src.ui.common.enums import FieldType

# "Single Source of Truth" for  column definitions.
COLUMN_MAP = {
    "RecID": FieldType.READONLY,
    "StatusDate": FieldType.READONLY,
    "FamilySerial": FieldType.TEXT,
    "CohortMemberID": FieldType.TEXT,
    "FirstName": FieldType.TEXT,
    "Surname": FieldType.TEXT,
    "Title": FieldType.TEXT,
    "Sex": FieldType.SEX_COMBOBOX,
    "DateOfBirth": FieldType.DATE,
    "Status": FieldType.READONLY,
    # You can add others if you want them to be explicit, 
    # otherwise they will default to TEXT in our logic.
}

# --- SEARCH CONFIGURATION ---
# Define which columns get a search box in the UI.
# Order matters: They will appear left-to-right.
SEARCH_FIELDS = ["Surname", "FirstName", "FamilySerial", "CohortMemberID"]


# --- TEMPORARY TEST SCHEMA ---
'''
COLUMN_MAP = {
    "AnimalID": FieldType.READONLY,
    "AnimalName": FieldType.TEXT,
    "Species": FieldType.TEXT,
    "StatusDate": FieldType.READONLY
}
'''