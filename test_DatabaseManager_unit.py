import unittest
import sqlite3
from DatabaseManager import DatabaseManager
from SQLiteDatabase import SQLiteDatabase

class TestDatabaseManager(unittest.TestCase):

    def tearDown(self):
        # Manually exit the context of DatabaseManager
        self.manager.__exit__(None, None, None)
        
    def setUp(self):
        # Create an instance of DatabaseManager, dependency inject connection, manually enter context
        
        database = SQLiteDatabase(":memory:").__enter__()
        self.manager = DatabaseManager(database).__enter__()

        # Create a test table
        self.manager.create_table("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
        """)

    def test_create_table(self):
        # Check if the table exists
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='test_table';"
        result = self.manager.database.execute_query(query)

        # Assert that the table was created
        self.assertTrue(len(result) > 0)
        
    def test_create_record(self):
        # Data to be inserted
        data = {'name': 'Test Name'}

        # Use the generalized create_record method to insert data
        insert_return = self.manager.create_record('test_table', data)

        # Check if the data is inserted
        select_query = "SELECT * FROM test_table WHERE name = ?;"
        result = self.manager.database.execute_query(select_query, (data['name'],))
        
        # Query to get the last inserted row ID
        last_id_query = "SELECT last_insert_rowid();"
        last_row_id = self.manager.database.execute_query(last_id_query)[0][0]

        # Assert that the data was inserted correctly
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Test Name')
        self.assertEqual(insert_return, last_row_id)

    def test_read_record(self):
        # Insert data for testing
        self.manager.create_record("test_table", {"name": "Sample Name"})
        
      # Query the data using retrieve_record method
        result = self.manager.retrieve_record("test_table", 1)

        # Assert that the query returns correct data
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Sample Name')

        
    def test_update_record(self):
        # Insert a record to update
        self.manager.create_record("test_table", {"name": "Old Name"})

        # Data to update the record
        updated_data = {'name': 'New Name'}

        # Update the record using the update_record method (to be implemented)
        # Replace the following line with the actual update method once it's implemented
        self.manager.update_record('test_table', 1, updated_data)

        # Query the updated data
        result = self.manager.retrieve_record("test_table", 1)

        # Assert that the record is updated correctly
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'New Name')

    def test_delete_record(self):
        # Insert a record to delete
        record_id = self.manager.create_record("test_table", {"name": "Test Name"})

        # Delete the record using the delete_record method (to be implemented)
        # Replace the following line with the actual delete method once it's implemented
        self.manager.delete_record('test_table', record_id)

        # Query the deleted record
        result = self.manager.retrieve_record("test_table", record_id)

        # Assert that the record is deleted correctly
        self.assertEqual(len(result), 0)
        
    
    def test_check_exists(self):
        # Create test data in the test_table
        self.manager.create_record("test_table", {"name": "Existing Name"})
        self.manager.create_record("test_table", {"name": "Another Name"})

        # Test for an existing attribute
        exists = self.manager.check_exists("test_table", "name", "Existing Name")
        self.assertTrue(exists)

        # Test for a non-existing attribute
        not_exists = self.manager.check_exists("test_table", "name", "Non-Existing Name")
        self.assertFalse(not_exists)
        
    def test_autoincrement(self):
        # Insert a record
        self.manager.create_record("test_table", {"name": "Test Name"})

        # Insert another record
        self.manager.create_record("test_table", {"name": "Another Name"})

        # Query the records
        result = self.manager.retrieve_record("test_table", 2)

        # Assert that the autoincrement works
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Another Test Name')

if __name__ == '__main__':
    unittest.main()