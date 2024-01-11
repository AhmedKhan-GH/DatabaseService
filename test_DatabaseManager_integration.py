import unittest
import os
import sqlite3
from SQLiteConnection import SQLiteConnection
from DatabaseManager import DatabaseManager

class TestDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        # Define the test database file name
        self.db_file = 'integration.db'
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_database_operations(self):
        # Initialize SQLiteConnection and DatabaseManager with the test database file
        with SQLiteConnection(self.db_file) as connection:
            with DatabaseManager(connection) as db_manager:

                # Create a test table
                db_manager.create_table("""
                    CREATE TABLE test (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT
                    );
                """)
                
                # Insert a record
                data_to_insert = {"name": "Integration Test"}
                db_manager.create_record("test", data_to_insert)

                # Retrieve the inserted record
                retrieved_record = db_manager.get_record("test", 1)

                # Ensure the record was inserted and retrieved correctly
                self.assertEqual(len(retrieved_record), 1)
                self.assertEqual(retrieved_record[0][1], "Integration Test")

                # Update the record
                updated_data = {"name": "Updated Test"}
                db_manager.update_record("test", 1, updated_data)

                # Retrieve the updated record
                updated_record = db_manager.get_record("test", 1)

                # Ensure the record was updated correctly
                self.assertEqual(len(updated_record), 1)
                self.assertEqual(updated_record[0][1], "Updated Test")

                # Delete the record
                db_manager.delete_record("test", 1)

                # Attempt to retrieve the deleted record
                deleted_record = db_manager.get_record("test", 1)

                # Ensure the record was deleted
                self.assertEqual(len(deleted_record), 0)

    def tearDown(self):
        # Delete the test database file
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

if __name__ == '__main__':
    unittest.main()