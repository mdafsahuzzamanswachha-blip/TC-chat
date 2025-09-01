from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet
import os

# Create a Flask web application instance.
app = Flask(__name__, template_folder='templates')
# Set a secret key for the application.
app.config['SECRET_KEY'] = 'my_secret_key'
# Initialize SocketIO for real-time communication.
socketio = SocketIO(app, async_mode='eventlet')

# Main page route.
@app.route('/')
def index():
    return render_template('index.html')

# This event is triggered when a new client connects.
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Handles new users joining the chat room.
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{username} has joined the room.', 'type': 'system'}, room=room)

# Handles incoming chat messages and broadcasts them.
@socketio.on('message')
def handle_message(data):
    print('Received message: ' + str(data))
    room = data['room']
    emit('message', data, room=room)

# Handles WebRTC signaling for video calls.
@socketio.on('signal')
def handle_signal(data):
    emit('signal', data, room=data['room'], skip_sid=request.sid)

# Main entry point to run the application.
if __name__ == '__main__':
    eventlet.monkey_patch()
    socketio.run(app, debug=True, port=int(os.environ.get('PORT', 5000)))
