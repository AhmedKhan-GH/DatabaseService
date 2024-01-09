import sqlite3

class SQLiteConnection :
    """
    A context manager class for managing SQLite database connections.

    Attributes:
        db_path (str): The path of the SQLite database file.
        connection (sqlite3.Connection): The SQLite connection object. Initially set to None.
    """
    
    def __init__(self, db_name):
        """
        Constructor, initializes a new instance of the SQLiteConnection class.

        Parameters:
            db_path (str): The path of the SQLite database file.
        """
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """
        Opens a connection to the SQLite database and returns it.

        This method is automatically called when entering the context of a 'with' statement.

        Returns:
            sqlite3.Connection: An open connection to the SQLite database.
        """
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the SQLite database connection.

        This method is automatically called when exiting the context of a 'with' statement.

        Parameters:
            exc_type (type): The type of the exception that occurred (if any).
            exc_val (Exception): The exception instance that occurred (if any).
            exc_tb (traceback): A traceback object representing the point in the code
                                where the exception occurred (if any).

        Returns:
            bool: False, to indicate that the method does not handle exceptions and
                  that any exception should be re-raised.
        """
        self.connection.close()
        return False
    
    def execute_query(self, query, params=None):
        """
        Executes a parameterized SQL query on the SQLite database.

        Parameters:
            query (str): The SQL query to execute.
            params (tuple, list, or dict, optional): The parameters to substitute into the query.

        Returns:
            list: The result of the query if it's a SELECT query, or an empty list for other query types.
        """
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
                else:
                    return cursor.rowcount
            
   
