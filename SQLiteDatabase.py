import sqlite3

class SQLiteDatabase :
   
    #constructor, sets database name and initializes connection variable awaiting enter
    def __init__(self, path):
        self.path = path
        self.connection = None

    #context entry, establishes connection to database file, returns class object
    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        return self

    #context exit, closes connection to database file, returns false to re-raise any exceptions
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        return False
    
    def execute_query(self, query, params=None):
        # Guard clause for query validation
        if not self.is_query_safe(query):
            raise ValueError("Query failed validation checks")

        cursor = self.connection.cursor()

        try:
            cursor.execute(query, params or ())  # Execute the query with sanitized parameters
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"SQL error occurred: {e}")

        # Guard clause for SELECT queries
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()

        # Handling non-SELECT queries
        self.connection.commit()
        if query.strip().upper().startswith("INSERT"):
            return cursor.lastrowid  # Return the last inserted row ID for INSERT queries

        return cursor.rowcount  # Return the row count for UPDATE/DELETE queries
    
    def is_query_safe(self, query):
        # Implement your validation logic here
        # For example, check for forbidden keywords or patterns
        forbidden_patterns = ["DROP", "ALTER"]
        for pattern in forbidden_patterns:
            if pattern in query:
                return False
        return True