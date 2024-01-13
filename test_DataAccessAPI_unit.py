import unittest
import json
import os
import DataAccessAPI
from DataAccessAPI import create_app  # Import your Flask app

class TestDataAccessAPI(unittest.TestCase):
    
    def setUp(self):
        
        # Creates a test client
        
        self.app = create_app('test.db')
        DataAccessAPI.create_table("""
                                   CREATE TABLE IF NOT EXISTS test 
                                   (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       name TEXT
                                   );
                                   """)
        
        # Propagate the exceptions to the test client
        self.app.testing = True
        
        self.client = self.app.test_client()
        
    def tearDown(self):
        self.app.db_manager.__exit__(None, None, None)
        self.app.db_manager.database.__exit__(None, None, None)
        
        if os.path.exists('test.db'):
            os.remove('test.db')
        

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Add more test cases here

    def test_create_record(self):
        # Define your test data
        data = {'name': 'Test Name'}
        # Send a POST request
        response = self.client.post('/create_record/test', data=json.dumps(data), content_type='application/json')
        # Check the response

        self.assertEqual(response.status_code, 201)

       
    # Add more test methods for other endpoints

if __name__ == '__main__':
    unittest.main()