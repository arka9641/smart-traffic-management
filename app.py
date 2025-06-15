from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv
from traffic_model import TrafficPredictor

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST')
)

# Initialize AI model
predictor = TrafficPredictor()

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sensors (sensor_id, location, current_vehicle_count, avg_speed) "
        "VALUES (%s, ST_Point(%s, %s), %s, %s)",
        (data['sensor_id'], data['longitude'], data['latitude'], 
         data['vehicle_count'], data['avg_speed'])
    )
    conn.commit()
    
    # Broadcast update
    socketio.emit('traffic_update', data)
    return jsonify({"status": "success"})

@app.route('/api/signals', methods=['GET'])
def get_signals():
    cur = conn.cursor()
    cur.execute("SELECT * FROM traffic_signals")
    return jsonify(cur.fetchall())

@app.route('/api/optimize-signal/<signal_id>', methods=['POST'])
def optimize_signal(signal_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensors ORDER BY timestamp DESC LIMIT 5")
    recent_data = cur.fetchall()
    
    # Get prediction (simplified)
    optimal_duration = predictor.predict(recent_data)
    
    cur.execute(
        "UPDATE traffic_signals SET current_duration = %s WHERE signal_id = %s",
        (optimal_duration, signal_id)
    )
    conn.commit()
    return jsonify({"new_duration": optimal_duration})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)