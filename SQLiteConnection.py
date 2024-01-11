import sqlite3

class SQLiteConnection :
   
    #constructor
    def __init__(self, db_name):
        #set data members
        self.db_name = db_name
        #connection needs initialization
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        return False
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()  # Create a cursor object using the connection
        cursor.execute(query, params or ())  # Execute the query with parameters
        
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()  # Return all fetched rows for SELECT queries
        else:
            self.connection.commit()  # Commit the transaction for non-SELECT queries
            return cursor.rowcount  # Return the row count for non-SELECT queries