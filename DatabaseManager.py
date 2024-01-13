
from SQLiteDatabase import SQLiteDatabase

class DatabaseManager :
    #constructor with dependency injection
    def __init__(self, database):
        self.database = database

    #upon context entry
    def __enter__(self):
        #set connection to sqlite3.connect object
        #return DatabaseManager object
        return self
        
    #upon context exit
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
    
    def print_table(self, table):
        # Create the select query
        select_query = f"SELECT * FROM {table};"

        # Execute the query
        result = self.database.execute_query(select_query)

        # Print the results
        for row in result:
            print(row, end="\n")
            
    def create_table(self, schema):
        # Check if the query starts with 'CREATE TABLE'
        if not schema.strip().upper().startswith("CREATE TABLE"):
            raise ValueError("The query does not start with 'CREATE TABLE'")
        else:
            # If the check passes, execute the query
            self.database.execute_query(schema)

    def create_record(self, table, data):
        # Construct column and placeholder strings
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))

        # Create the SQL query
        insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"

        # Execute the query
        return self.database.execute_query(insert_query, tuple(data.values()))

    def retrieve_record(self, table, record_id):
        
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

    def check_exists(self, table, column, attribute):
        """
        Check if a given attribute exists in a specified column of a table.
        
        :param table: The table to check in.
        :param column: The column to look through.
        :param attribute: The attribute to check for.
        :return: True if the attribute exists, False otherwise.
        """
        # Construct the SQL query
        check_query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {column} = ? LIMIT 1);"

        # Execute the query and get result
        result = self.database.execute_query(check_query, (attribute,))

        # extract the boolean value
        return result[0][0] == 1 