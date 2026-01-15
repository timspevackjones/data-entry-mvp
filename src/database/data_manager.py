from pyodbc import connect
from os import getenv
from dotenv import load_dotenv


class DataManager:
    def __init__(self):
        load_dotenv()
        self.conn_string = getenv("SQL_CONNECTION_STRING")

        # --- CONFIGURATION SECTION ---
        self.table_name = "tblCohortMember" # Was "tblTestAnimals" for temp testing
        # this is the Identity column 
        self.primary_key_col = "RecID" # Was "AnimalID" for temp testing
        
        # OPTIONAL: Set a specific sort order (e.g., "Surname, FirstName")
        # If you leave this as None, it defaults to sorting by the Primary Key.        
        self.db_sort_order = "RecID, FamilySerial, CohortMemberID"

        # Define which fields to ignore when updating
        # can add other fields to ignore here if needed
        self.ignored_columns = ["AnimalID", "StatusDate", "Status"]

    def _get_connection(self):
        """Helper method to get a fresh connection every time"""
        return connect(self.conn_string)

    def get_all_records(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # LOGIC: Use the custom sort if it exists, otherwise use Primary Key
        sort_col = self.db_sort_order if self.db_sort_order else self.primary_key_col

        # TODO: ability to select 1000 more
        query = f"""
            SELECT TOP 1000 * FROM {self.table_name}
            ORDER BY {sort_col}
        """

        cursor.execute(query)

        # 1. Get the Column Names (Headers)
        # cursor.description is a tuple of tuples.
        # We just want the first item (name) from each.
        headers = [column[0] for column in cursor.description]

        # 2. Get the Data
        records = cursor.fetchall()
        # Clean up
        conn.close()

        # Convert to list of lists for the UI
        return headers, [list(row) for row in records]

    def update_record(
        self, row_dict
    ):
        """
        Updates a single record in the database based on RecID.
        Returns: (Success_Boolean, Message_String)
        """
        conn = self._get_connection()
        cursor = conn.cursor()


        try:
            # 2. Extract PrimaryKey <-- Primary Key update if changes
            primary_key = row_dict.get(self.primary_key_col)
            if not primary_key:
                return False, f"Critical Error: Row is missing {self.primary_key_col}."

            # 4. Filter the dictionary to get only the columns we want to update
            valid_keys = [k for k in row_dict.keys() if k not in self.ignored_columns and k != self.primary_key_col]

            if not valid_keys:
                return False, "No changes detected or valid columns to update."
            
            # 5. Build the SQL Query Dynamically
            # Step A: Create the "Field=?" strings
            set_parts = [f"{key}=?" for key in valid_keys]

            # Step B: Join them with commas( "Surname=?, FirstName=?")
            set_clause = ", ".join(set_parts)

            # Step C: Form the full query
            # Always update StatusDate=GETDATE()
            query = f"UPDATE {self.table_name} SET {set_clause}, StatusDate=GETDATE() WHERE {self.primary_key_col}=?"

            # 6. Prepare the values list, in same order as valid_keys
            values = [row_dict[key] for key in valid_keys]
            
            # Add RecID at the end for the "WHERE RecID=?" part
            values.append(primary_key)

            # 7. Execute
            cursor.execute(query, values)
            conn.commit()

            return True, "Success"

        except Exception as e:
            return False, str(e)

        finally:
            # 8. Clean up
            conn.close()

    def search_records(self, search_params):
        """
        Searches records based on search_params dictionary.
        search_dict example: {'Surname': 'Smith', 'FamilySerial': '123'}
        Returns: (headers, records)       
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # 1. Start with a base query that is always true (WHERE 1=1)
            sort_col = self.db_sort_order if self.db_sort_order else self.primary_key_col
            base_query = f"SELECT TOP 1000 * FROM {self.table_name} WHERE 1=1"
            
            values = []
            conditions = []

            # 2. Loop through the dictionary and build the "AND Col LIKE ?" parts
            for col, search_term in search_params.items():
                if search_term: # Only add if user actually typed something
                    # We use generic syntax. 
                    # SQL Server 'LIKE' is case-insensitive by default.
                    conditions.append(f"{col} LIKE ?")
                    
                    # Wrap the term in %...% for wildcard search (contains)
                    values.append(f"%{search_term}%")

            # 3. Combine it
            if conditions:
                # Join them: "AND Surname LIKE ? AND FamilySerial LIKE ?"
                full_where = " AND ".join(conditions)
                query = f"{base_query} AND {full_where} ORDER BY {sort_col}"
            else:
                # If search is empty, just return the normal top 1000
                query = f"{base_query} ORDER BY {sort_col}"

            # 4. Execute
            # print(f"DEBUG SEARCH: {query} with {values}")
            cursor.execute(query, values)

            headers = [column[0] for column in cursor.description]
            records = cursor.fetchall()

            return headers, [list(row) for row in records]

        finally:
            conn.close()
    
    def add_record(self, data_dict):
        """
        Adds a new record to the database.
        data_dict: dictionary of column names and their values.
        Returns: (Success_Boolean, Message_String)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # 1. Filter out any keys that aren't in the data_dict (safety check)
            # We only insert columns that actually have data
            columns = [k for k in data_dict.keys()]
            
            if not columns:
                return False, "No data provided."

            # 2. Build the query
            # Result: "INSERT INTO tblCohortMember (Surname, FirstName) VALUES (?, ?)"
            col_str = ", ".join(columns)
            
            # Create a string of question marks: "?, ?, ?" matching the number of columns
            placeholders = ", ".join(["?" for _ in columns])
            
            query = f"INSERT INTO {self.table_name} ({col_str}) VALUES ({placeholders})"
            
            # 3. Prepare values in the correct order
            values = [data_dict[col] for col in columns]

            cursor.execute(query, values)
            conn.commit()

            return True, "Successfully added record."

        except Exception as e:
            return False, str(e)
            
        finally:
            conn.close()


if __name__ == "__main__":
    dm = DataManager()
    print(dm.get_all_records())
