from pyodbc import connect
from os import getenv
from dotenv import load_dotenv



class DataManager:
    def __init__(self):
        load_dotenv()
        self.conn_string = getenv("SQL_CONNECTION_STRING")
    
    def _get_connection(self):
        """Helper method to get a fresh connection every time"""
        return connect(self.conn_string)

    def get_all_records(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # TODO: ability to select 1000 more
        query = """
            SELECT TOP 1000 * FROM tblCohortMember 
            ORDER BY RecID, FamilySerial, CohortMemberID
        """

        cursor.execute(query)

        # 1. Get the Column Names (Headers)
        # cursor.description is a tuple of tuples. We just want the first item (name) from each.
        headers = [column[0] for column in cursor.description]
        
        # 2. Get the Data
        records = cursor.fetchall()
        # Clean up
        conn.close()

        # Convert to list of lists for the UI
        return headers, [list(row) for row in records]

    def update_record(self, rec_id, family, member_id, surname, first, title, sex, dob, status):
        """
        Updates a single record in the database based on RecID.
        Returns: (Success_Boolean, Message_String)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # We use '?' placeholders to prevent SQL Injection
            query = """
                UPDATE tblCohortMember
                SET FamilySerial=?, CohortMemberID=?, Surname=?, FirstName=?, 
                    Title=?, Sex=?, DateOfBirth=?, Status=?, StatusDate=GETDATE()
                WHERE RecID=?
            """
            
            # Execute the query with the variables
            cursor.execute(query, (family, member_id, surname, first, title, sex, dob, status, rec_id))
            conn.commit()
            
            return True, "Success"
            
        except Exception as e:
            return False, str(e)
            
        finally:
            conn.close()
        

if __name__ == "__main__":
    dm = DataManager()
    print(dm.get_all_records())

