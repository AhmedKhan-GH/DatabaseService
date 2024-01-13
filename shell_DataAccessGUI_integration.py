import unittest
import threading
import json
import os
import time
from DataAccessAPI import DataAccessAPI
from DataAccessGUI import DataAccessGUI
from DatabaseManager import DatabaseManager
from SQLiteDatabase import SQLiteDatabase

class TestFullApplication(unittest.TestCase):

    def setUp(self):
    #test database file cleanup
        self.path = "test.db"
        if os.path.exists(self.path):
            os.remove(self.path)
        
        #dependency injection chain
        database = SQLiteDatabase(self.path).__enter__()
        manager = DatabaseManager(database).__enter__()
        api = DataAccessAPI(manager).__enter__()
        self.gui = DataAccessGUI(api, enable_gui=True).__enter__()
        
        # Creates a test client
        self.gui.api.manager.create_table("""
            CREATE TABLE IF NOT EXISTS test 
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
            """)
        
        # Propagate the exceptions to the test client
        self.gui.api.server.testing = True
        
        self.client = self.gui.api.server.test_client()
  
        
    def tearDown(self):

        self.gui.api.manager.database.__exit__(None, None, None)
        self.gui.api.manager.__exit__(None, None, None)
        self.gui.api.__exit__(None, None, None)
        self.gui.__exit__(None, None, None)

        if os.path.exists(self.path):
            os.remove(self.path)

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_dash_route(self):
        if self.gui.enable_gui:
            response = self.client.get('/dash/')
            self.assertEqual(response.status_code, 200)
        else:
            self.assertTrue(1)
        # Add more assertions as needed

    # Other test methods can be added here to test different functionalities

if __name__ == '__main__':
    unittest.main()
    
