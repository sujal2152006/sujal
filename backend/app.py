from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/museum'))
db = client['museum']

API_KEY = os.getenv('API_KEY')

def verify_api_key():
    return request.headers.get('X-API-Key') == API_KEY

@app.route('/api/login', methods=['POST'])
def login():
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    user = db.users.find_one({'email': data['email']})
    
    if user and check_password_hash(user['password'], data['password']):
        return jsonify({
            'success': True,
            'user': {
                'email': user['email'],
                'role': user['role'],
                'name': user['name']
            }
        })
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/tickets', methods=['GET', 'POST'])
def tickets():
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        ticket = request.json
        ticket['created_at'] = datetime.utcnow()
        result = db.tickets.insert_one(ticket)
        return jsonify({'id': str(result.inserted_id), 'success': True})
    
    tickets = list(db.tickets.find())
    for t in tickets:
        t['_id'] = str(t['_id'])
    return jsonify(tickets)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
