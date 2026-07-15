from flask import Flask, jsonify,request
from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('mongo_uri'))

app=Flask(__name__)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = json.loads(request.data)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    db = client['mydatabase']
    users_collection = db['users']

    signup_data = {
        'email': email,
        'password': password
    }

    users_collection.insert_one(signup_data)
    return jsonify({'message': 'Data submitted successfully'}), 200

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json(silent=True) or request.form
    item_name = data.get('itemName')
    item_description = data.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({
            'error': 'itemName and itemDescription are required'
        }), 400

    todo_item = {
        'itemName': item_name.strip(),
        'itemDescription': item_description.strip()
    }

    if not todo_item['itemName'] or not todo_item['itemDescription']:
        return jsonify({
            'error': 'itemName and itemDescription cannot be empty'
        }), 400

    db = client['mydatabase']
    todos_collection = db['todos']
    result = todos_collection.insert_one(todo_item)

    return jsonify({
        'message': 'To-do item submitted successfully',
        'id': str(result.inserted_id)
    }), 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)
