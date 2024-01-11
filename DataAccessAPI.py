from flask import Flask, request, jsonify
import os
from SQLiteConnection import SQLiteConnection
from DatabaseManager import DatabaseManager



# Initialize your database connection

app = Flask(__name__)

def create_app(db_path):
    connection = SQLiteConnection(db_path).__enter__()
    app.db_manager = DatabaseManager(connection).__enter__()
    return app
    
def create_table(schema):
    app.db_manager.create_table(schema)

@app.route('/create_record/<table>', methods=['POST'])
def create_record(table):
    data = request.get_json()
    app.db_manager.create_record(table, data)
    return jsonify({"message": "Record created successfully."}), 201

@app.route('/')
def root():
    return jsonify({"message": "Hello World!"}), 200

"""
@app.route('/get_record/<table>/<int:record_id>', methods=['GET'])
def get_record(table, record_id):
    with database_manager:
        record = database_manager.get_record(table, record_id)
    return jsonify(record)

@app.route('/update_record/<table>/<int:record_id>', methods=['PUT'])
def update_record(table, record_id):
    data = request.json
    with database_manager:
        database_manager.update_record(table, record_id, data)
    return jsonify({"message": "Record updated successfully."})

@app.route('/delete_record/<table>/<int:record_id>', methods=['DELETE'])
def delete_record(table, record_id):
    with database_manager:
        database_manager.delete_record(table, record_id)
    return jsonify({"message": "Record deleted successfully."})

@app.route('/print_table/<table>', methods=['GET'])
def print_table(table):
    with database_manager:
        records = database_manager.print_table(table)
    return jsonify(records)
"""        


if __name__ == '__main__':
    app.run()