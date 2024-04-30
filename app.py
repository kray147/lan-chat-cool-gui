from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

connected_users = set()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    connected_users.add(request.sid)
    emit('user_connected', {'user_count': len(connected_users)}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    connected_users.remove(request.sid)
    emit('user_connected', {'user_count': len(connected_users)}, broadcast=True)

@socketio.on('chat message')
def handle_message(data):
    sender = data['sender']
    message = data['message']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  

    emit('chat message', {'sender': sender, 'message': message, 'timestamp': timestamp}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2000, debug=True, allow_unsafe_werkzeug=True )
