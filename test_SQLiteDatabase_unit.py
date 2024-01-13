import unittest
import sqlite3
from SQLiteDatabase import SQLiteDatabase

class TestSQLiteDatabase(unittest.TestCase):
        
    def setUp(self):
        self.database = SQLiteDatabase(":memory:").__enter__()
        self.database.execute_query("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    
    def tearDown(self):
        # Clean up and close the database database
        self.database.__exit__(None, None, None)

    def test_query_execution(self):
        # Execute a simple SELECT query
        result = self.database.execute_query("SELECT 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)
    import sqlite3

    def test_syntax_error(self):
        try:
            self.database.execute_query("SELEC * FROM test")  # Intentional typo in query
            self.fail("Expected Exception, but no exception was raised.")
        except Exception:
            # The test passes if an exception is raised
            pass

    def test_banned_query(self):
        try:
            self.database.execute_query("DROP TABLE test")
            self.fail("Expected ValueError, but no exception was raised.")
        except ValueError:
            # The test passes if a ValueError is raised
            pass

    def test_select_query(self):
        # Insert some data
        self.database.execute_query("INSERT INTO test (name) VALUES (?)", ("Test Name",))

        # Execute a SELECT query
        result = self.database.execute_query("SELECT * FROM test")
        self.assertEqual(len(result), 1)  # Verify that one row is returned
        self.assertEqual(result[0][1], "Test Name")  # Verify the data in the row
        
    def test_insert_query(self):
        # Execute an INSERT query
        insert_return = self.database.execute_query("INSERT INTO test (name) VALUES (?)", ("Test Name",))

        # Query to get the last inserted row ID
        last_id_query = "SELECT last_insert_rowid();"
        last_row_id = self.database.execute_query(last_id_query)[0][0]

        self.assertEqual(insert_return, last_row_id)

        # Verify data insertion with a SELECT query
        result = self.database.execute_query("SELECT * FROM test WHERE name = ?", ("Test Name",))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Test Name")

    def test_update_query(self):
        # Insert initial data
        self.database.execute_query("INSERT INTO test (name) VALUES (?)", ("Old Name",))

        # Execute an UPDATE query
        row_count = self.database.execute_query("UPDATE test SET name = ? WHERE name = ?", ("New Name", "Old Name"))
    
        # Verify that one row was updated
        self.assertEqual(row_count, 1)

        # Verify data update with a SELECT query
        result = self.database.execute_query("SELECT * FROM test WHERE name = ?", ("New Name",))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "New Name")
        
    def test_delete_query(self):
        # Insert data to delete
        self.database.execute_query("INSERT INTO test (name) VALUES (?)", ("Test Name",))

        # Execute a DELETE query
        row_count = self.database.execute_query("DELETE FROM test WHERE name = ?", ("Test Name",))
    
        # Verify that one row was deleted
        self.assertEqual(row_count, 1)

        # Verify data deletion with a SELECT query
        result = self.database.execute_query("SELECT * FROM test WHERE name = ?", ("Test Name",))
        self.assertEqual(len(result), 0)

    def test_sql_injection(self):
        # Insert dummy data
        self.database.execute_query("INSERT INTO test (name) VALUES (?)", ("Dummy",))

        # Malicious input attempting to alter the database
        malicious_input = "Dummy'); DROP TABLE test;"
        self.database.execute_query("INSERT INTO test (name) VALUES (?)", (malicious_input,))

        # Verify that the malicious input is not executed
        result = self.database.execute_query("SELECT * FROM test")
        self.assertTrue(any("Dummy" in row for row in result))
        self.assertTrue(any(malicious_input in row for row in result))
        self.assertTrue(len(result) > 1)  # More than one record should exist

if __name__ == "__main__":
    unittest.main()
