from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('request_update')
def handle_update_request():
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensors ORDER BY timestamp DESC LIMIT 10")
    emit('traffic_update', cur.fetchall())