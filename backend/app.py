from flask import Flask, request, jsonify
from flask_cors import CORS
from sentiment import analyze_sentiment
from allocation import predict_allocation
from backtest import run_backtest
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory user store (for demo purposes only)
users = {}

# --- AUTHENTICATION ENDPOINTS ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'success': False, 'message': 'Missing email or password'}), 400
    if email in users:
        return jsonify({'success': False, 'message': 'User already exists'}), 409
    users[email] = password
    return jsonify({'success': True, 'message': 'Registration successful!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if users.get(email) == password:
        return jsonify({'success': True, 'message': 'Login successful!'})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# --- AI FEATURE ENDPOINTS ---

@app.route('/sentiment', methods=['POST'])
def sentiment_api():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    result = analyze_sentiment(text)
    return jsonify(result)

@app.route('/allocation', methods=['POST'])
def allocation_api():
    data = request.get_json()
    text = data.get('text')
    avg_return = data.get('avg_return')
    cluster = data.get('cluster')
    if not all([text, avg_return, cluster]):
        return jsonify({'error': 'Text, avg_return, and cluster are required'}), 400
    result = predict_allocation(text, float(avg_return), int(cluster))
    return jsonify(result)

@app.route('/backtest', methods=['POST'])
def backtest_api():
    data = request.get_json()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if not all([start_date, end_date]):
        return jsonify({'error': 'Start date and end date are required'}), 400
    result = run_backtest(start_date, end_date)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
