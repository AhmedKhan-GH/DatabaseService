import unittest
import json
import os
from DataAccessAPI import DataAccessAPI
from DatabaseManager import DatabaseManager # Import your Flask server
from SQLiteDatabase import SQLiteDatabase

class TestDataAccessAPI(unittest.TestCase):
    
    def setUp(self):
        #test database file cleanup
        self.path = "test.db"
        if os.path.exists(self.path):
            os.remove(self.path)
        
        #dependency injection chain
        database = SQLiteDatabase(self.path).__enter__()
        manager = DatabaseManager(database).__enter__()
        self.api = DataAccessAPI(manager).__enter__()
        
        # Creates a test client
        self.api.manager.create_table("""
                                   CREATE TABLE IF NOT EXISTS test 
                                   (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       name TEXT
                                   );
                                   """)
        
        # Propagate the exceptions to the test client
        self.api.server.testing = True
        
        self.client = self.api.server.test_client()
        
    def tearDown(self):
        self.api.manager.database.__exit__(None, None, None)
        self.api.manager.__exit__(None, None, None)
        self.api.__exit__(None, None, None)
        if os.path.exists(self.path):
            os.remove(self.path)
       
    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Add more test cases here

    def test_create_record(self):
        # Define your test data
        data = {'name': 'Test Name'}
        # Send a POST request
        response = self.client.post('/create_record/test', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.get_json()["record_id"], 1)
        # Check the response

        self.assertEqual(response.status_code, 201)
        
    def test_print_table(self):
        insert_data_1 = {'name': 'Test Name 1'}
        insert_data_2 = {'name': 'Test Name 2'}
        create_record_response_1 = self.client.post('/create_record/test', data=json.dumps(insert_data_1), content_type='application/json')
        create_record_response_2 = self.client.post('/create_record/test', data=json.dumps(insert_data_2), content_type='application/json')
        
        self.assertEqual(create_record_response_1.status_code, 201)
        self.assertEqual(create_record_response_1.get_json()["record_id"], 1)
        
        self.assertEqual(create_record_response_2.status_code, 201)
        self.assertEqual(create_record_response_2.get_json()["record_id"], 2)

        print_table_response = self.client.get('/get_table/test')
        
        self.assertEqual(insert_data_1['name'], json.loads(print_table_response.data.decode('utf-8'))[0][1])
        self.assertEqual(insert_data_2['name'], json.loads(print_table_response.data.decode('utf-8'))[1][1])
    
        self.assertEqual(print_table_response.status_code, 200)

    # Add more test methods for other endpoints

if __name__ == '__main__':
    unittest.main()