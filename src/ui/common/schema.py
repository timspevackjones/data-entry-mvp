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
    "StatusDate": FieldType.READONLY
    # You can add others if you want them to be explicit, 
    # otherwise they will default to TEXT in our logic.
}