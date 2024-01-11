
from SQLiteConnection import SQLiteConnection

class DatabaseManager :
    #constructor
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    #upon context entry
    def __enter__(self):
        #set database to SQLiteConnection object
        self.database = SQLiteConnection(self.db_path)
        #set connection to sqlite3.connect object
        self.database.__enter__()
        #return DatabaseManager object
        return self
        
    #upon context exit
    def __exit__(self, exc_type, exc_val, exc_tb):
        #call __exit__ method of SQLiteConnection
        #with appropriate data
        return self.database.connection.__exit__(exc_type, exc_val, exc_tb)

    def print_table(self, table):
        # Create the select query
        select_query = f"SELECT * FROM {table};"

        # Execute the query
        result = self.database.execute_query(select_query)

        # Print the results
        for row in result:
            print(row)

    def create_table(self, schema):
        self.database.execute_query(schema)

    def create_record(self, table, data):
        # Construct column and placeholder strings
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))

        # Create the SQL query
        insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"

        # Execute the query
        self.database.execute_query(insert_query, tuple(data.values()))

    def get_record(self, table, record_id):
        
        select_query = f"SELECT * FROM {table} WHERE id = ?;"

        return self.database.execute_query(select_query, (record_id,))

    def update_record(self, table, record_id, data):
        # Construct the SET clause for updating columns
        set_clause = ', '.join([f"{column} = ?" for column in data.keys()])

        # Create the SQL query for updating the record
        update_query = f"UPDATE {table} SET {set_clause} WHERE id = ?;"

        # Execute the query to update the record
        self.database.execute_query(update_query, tuple(data.values()) + (record_id,))

    def delete_record(self, table, record_id):
        # Create the SQL query for deleting the record
        delete_query = f"DELETE FROM {table} WHERE id = ?;"

        # Execute the query to delete the record
        self.database.execute_query(delete_query, (record_id,))