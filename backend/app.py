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
if __name__ == '__main__':
    app.run(port=5000, debug=True)