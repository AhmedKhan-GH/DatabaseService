import unittest
from unittest.mock import Mock, patch
from SQLiteConnection import SQLiteConnection

class TestSQLiteConnection(unittest.TestCase):
    
    #patch decorator to mock the sqlite3.connect() function
    @patch('SQLiteConnection.sqlite3.connect')
    
    def test_init(self, mock_connect):
        
        # Configure the mock_connect to return a mock connection
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        # Create an instance of SQLiteConnection
        db_name = "test.db"
        connection = SQLiteConnection(db_name)
        
        # Verify that __init__ method sets the db_name attribute
        self.assertEqual(connection.db_name, db_name)
        self.assertIsNone(connection.connection)


    @patch('SQLiteConnection.sqlite3.connect')
    def test_enter(self, mock_connect):

        # Configure the mock_connect to return the mock_connection
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        # Create an instance of SQLiteConnection
        # Enter the context using a 'with' statement
        db_name = "test.db"
        with SQLiteConnection(db_name) as connection:
            # Verify that __enter__ method opens a connection
            self.assertEqual(connection, mock_connection)

        # Ensure that the connection is closed after exiting the 'with' block
        mock_connection.close.assert_called_once()

    @patch('SQLiteConnection.sqlite3.connect')
    def test_exit_exception(self, mock_connect):
        
        # Configure the mock_connect to return a mock connection
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        # Create an instance of SQLiteConnection
        connection_obj = SQLiteConnection("test.db")

        # Manually invoke the __enter__ to get the mock connection
        connection_obj.__enter__()

        # Simulate an exception info, you can adjust these as needed
        exc_type, exc_val, exc_tb = Exception, Exception("error"), object()

        # Manually invoke __exit__ with simulated exception info
        return_value = connection_obj.__exit__(exc_type, exc_val, exc_tb)

        # Check that the connection's close method was called
        mock_connection.close.assert_called_once()

        # Check that the __exit__ method returns False
        self.assertFalse(return_value)

    @patch('SQLiteConnection.sqlite3.connect')
    def test_exit_success(self, mock_connect):
        
        # Create a mock connection object
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        # Create an instance of SQLiteConnection
        connection_obj = SQLiteConnection("test.db")

        # Manually invoke the __enter__ to get the mock connection
        connection_obj.__enter__()

        # Manually invoke __exit__ without any exception (None values)
        return_value = connection_obj.__exit__(None, None, None)

        # Check that the connection's close method was called
        mock_connection.close.assert_called_once()

        # Check that the __exit__ method returns False (which means it's not handling the exception)
        self.assertFalse(return_value)

if __name__ == "__main__":
    unittest.main()
