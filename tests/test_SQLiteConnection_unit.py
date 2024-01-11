import unittest
import sqlite3
from SQLiteConnection import SQLiteConnection

class TestSQLiteConnection(unittest.TestCase):
        
    def setUp(self):
        # Set up a temporary database for testing
        self.db_name = ":memory:"  # Use an in-memory database
        self.connection = SQLiteConnection(self.db_name)
        self.connection.__enter__()
        self.connection.execute_query("CREATE TABLE test (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")

    def test_query_execution(self):
        # Execute a simple SELECT query
        result = self.connection.execute_query("SELECT 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)
    
    def test_query_syntax_error(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.connection.execute_query("SELEC * FROM test")  # Intentional typo in query

    def test_select_query(self):
        # Insert some data
        self.connection.execute_query("INSERT INTO test (name) VALUES (?)", ("Select Test Name",))

        # Execute a SELECT query
        result = self.connection.execute_query("SELECT * FROM test")
        self.assertEqual(len(result), 1)  # Verify that one row is returned
        self.assertEqual(result[0][1], "Select Test Name")  # Verify the data in the row
        
    def test_insert_query(self):
        # Execute an INSERT query
        row_count = self.connection.execute_query("INSERT INTO test (name) VALUES (?)", ("Insert Test Name",))
    
        # Verify that one row was inserted
        self.assertEqual(row_count, 1)

        # Verify data insertion with a SELECT query
        result = self.connection.execute_query("SELECT * FROM test WHERE name = ?", ("Insert Test Name",))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Insert Test Name")

    def test_update_query(self):
        # Insert initial data
        self.connection.execute_query("INSERT INTO test (name) VALUES (?)", ("Old Update Name",))

        # Execute an UPDATE query
        row_count = self.connection.execute_query("UPDATE test SET name = ? WHERE name = ?", ("New Update Name", "Old Update Name"))
    
        # Verify that one row was updated
        self.assertEqual(row_count, 1)

        # Verify data update with a SELECT query
        result = self.connection.execute_query("SELECT * FROM test WHERE name = ?", ("New Update Name",))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "New Update Name")
        
    def test_delete_query(self):
        # Insert data to delete
        self.connection.execute_query("INSERT INTO test (name) VALUES (?)", ("Test Delete Name",))

        # Execute a DELETE query
        row_count = self.connection.execute_query("DELETE FROM test WHERE name = ?", ("Test Delete Name",))
    
        # Verify that one row was deleted
        self.assertEqual(row_count, 1)

        # Verify data deletion with a SELECT query
        result = self.connection.execute_query("SELECT * FROM test WHERE name = ?", ("Test Delete Name",))
        self.assertEqual(len(result), 0)

    def test_sql_injection_protection(self):
        # Insert dummy data
        self.connection.execute_query("INSERT INTO test (name) VALUES (?)", ("Dummy",))

        # Malicious input attempting to alter the database
        malicious_input = "Dummy'); DELETE FROM test; --"
        self.connection.execute_query("INSERT INTO test (name) VALUES (?)", (malicious_input,))

        # Verify that the malicious input is not executed
        result = self.connection.execute_query("SELECT * FROM test")
        self.assertTrue(any("Dummy" in row for row in result))
        self.assertTrue(any(malicious_input in row for row in result))
        self.assertTrue(len(result) > 1)  # More than one record should exist
    def tearDown(self):
        # Clean up and close the database connection
        self.connection.__exit__(None, None, None)

if __name__ == "__main__":
    unittest.main()
