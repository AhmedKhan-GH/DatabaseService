import unittest
import sqlite3
from DatabaseManager import DatabaseManager
from SQLiteConnection import SQLiteConnection

class TestDatabaseManager(unittest.TestCase):

    def tearDown(self):
        # Manually exit the context of DatabaseManager
        self.db_manager.__exit__(None, None, None)
        
    def setUp(self):
        # Create an instance of DatabaseManager, dependency inject connection, manually enter context
        self.db_manager = DatabaseManager(SQLiteConnection(":memory:"))
        self.db_manager.__enter__()

        # Create a test table
        self.db_manager.create_table("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
        """)

    def test_create_table(self):
        # Check if the table exists
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='test_table';"
        result = self.db_manager.database.execute_query(query)

        # Assert that the table was created
        self.assertTrue(len(result) > 0)
        
    def test_create_record(self):
        # Data to be inserted
        data = {'name': 'Test Name'}

        # Use the generalized create_record method to insert data
        self.db_manager.create_record('test_table', data)

        # Check if the data is inserted
        select_query = "SELECT * FROM test_table WHERE name = ?;"
        result = self.db_manager.database.execute_query(select_query, (data['name'],))

        # Assert that the data was inserted correctly
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Test Name')

    def test_read_record(self):
        # Insert data for testing
        self.db_manager.create_record("test_table", {"name": "Sample Name"})
        
      # Query the data using get_record method
        result = self.db_manager.get_record("test_table", 1)

        # Assert that the query returns correct data
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Sample Name')

        
    def test_update_record(self):
        # Insert a record to update
        self.db_manager.create_record("test_table", {"name": "Old Name"})

        # Data to update the record
        updated_data = {'name': 'New Name'}

        # Update the record using the update_record method (to be implemented)
        # Replace the following line with the actual update method once it's implemented
        self.db_manager.update_record('test_table', 1, updated_data)

        # Query the updated data
        result = self.db_manager.get_record("test_table", 1)

        # Assert that the record is updated correctly
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'New Name')

    def test_delete_record(self):
        # Insert a record to delete
        self.db_manager.create_record("test_table", {"name": "Record to Delete"})

        # Delete the record using the delete_record method (to be implemented)
        # Replace the following line with the actual delete method once it's implemented
        self.db_manager.delete_record('test_table', 1)

        # Query the deleted record
        result = self.db_manager.get_record("test_table", 1)

        # Assert that the record is deleted correctly
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()