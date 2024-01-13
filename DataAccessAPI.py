from SQLiteDatabase import SQLiteDatabase
from DatabaseManager import DatabaseManager

# Initialize your database connection

from flask import Flask, request, jsonify

class DataAccessAPI:
    def __init__(self, manager):
        self.server = Flask(__name__)
        self.manager = manager
        self.add_routes()
        
    def __enter__(self):
        return self 

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def add_routes(self):
        
        @self.server.route('/shutdown', methods=['POST'])
        def shutdown():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()
            return

        @self.server.route('/create_record/<table>', methods=['POST'])
        def create_record(table):
            data = request.get_json()
            record_id = self.manager.create_record(table, data)
            return jsonify({"message": "Record created successfully.", "record_id": record_id}), 201

        @self.server.route('/')
        def root():
            return jsonify({"message": "Welcome to DataAccessAPI"}), 200

        @self.server.route('/retrieve_record/<table>/<int:record_id>', methods=['GET'])
        def retrieve_record(table, record_id):
            record = self.manager.retrieve_record(table, record_id)
            return jsonify(record)

        @self.server.route('/update_record/<table>/<int:record_id>', methods=['PUT'])
        def update_record(table, record_id):
            data = request.json
            count = self.manager.update_record(table, record_id, data)
            return jsonify({"message": f"{count} record(s) updated successfully."}), 200

        @self.server.route('/delete_record/<table>/<int:record_id>', methods=['DELETE'])
        def delete_record(table, record_id):
            count = self.manager.delete_record(table, record_id)
            return jsonify({"message": f"{count} record(s) deleted successfully."}), 200

        @self.server.route('/get_table/<table>', methods=['GET'])
        def print_table(table):
            records = self.manager.get_table(table)
            return jsonify(records)

    def run(self, host='0.0.0.0', port=5000):
        self.server.run(host=host, port=port)
        