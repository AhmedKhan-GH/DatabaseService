import unittest
import os
import sqlite3
from SQLiteDatabase import SQLiteDatabase
from DatabaseManager import DatabaseManager

class TestDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        # Define the test database file name
        self.db_file = 'integration.db'
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_database_operations(self):
        # Initialize SQLiteDatabase and DatabaseManager with the test database file
        with SQLiteDatabase(self.db_file) as connection:
            with DatabaseManager(connection) as db_manager:

                # Create a test table
                db_manager.create_table("""
                    CREATE TABLE IF NOT EXISTS test 
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT
                    );""")
                
                # Insert a record
                record_id = db_manager.create_record("test", {"name": "Integration Test"})

                # Retrieve the inserted record
                retrieved_record = db_manager.retrieve_record("test", record_id)

                # Ensure the record was inserted and retrieved correctly
                self.assertEqual(len(retrieved_record), 1)
                self.assertEqual(retrieved_record[0][1], "Integration Test")

                # Update the record
                db_manager.update_record("test", record_id, {"name": "Updated Test"})

                # Retrieve the updated record
                updated_record = db_manager.retrieve_record("test", record_id)

                # Ensure the record was updated correctly
                self.assertEqual(len(updated_record), 1)
                self.assertEqual(updated_record[0][1], "Updated Test")

                # Delete the record
                db_manager.delete_record("test", record_id)

                # Attempt to retrieve the deleted record
                deleted_record = db_manager.retrieve_record("test", record_id)

                # Ensure the record was deleted
                self.assertEqual(len(deleted_record), 0)

    def tearDown(self):
        # Delete the test database file
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

if __name__ == '__main__':
    unittest.main()