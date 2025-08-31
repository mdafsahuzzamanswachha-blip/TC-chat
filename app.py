from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionary to map session ids to nicknames (simplified for 2-person chat)
clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    clients[request.sid] = "Anonymous"

@socketio.on('set_nickname')
def handle_nickname(nickname):
    clients[request.sid] = nickname

@socketio.on('message')
def handle_message(data):
    try:
        data = json.loads(data)
    except:
        data = {"msg": str(data), "nickname": "Anonymous", "image": ""}

    msg = data.get("msg", "")
    nickname = clients.get(request.sid, "Anonymous")
    image = data.get("image", "")
    
    full_msg = f"{nickname}: {msg}"
    if image:
        full_msg += f" <img src='{image}' style='max-width:200px; display:block;'/>"

    # Broadcast only to other clients (2-person chat)
    for sid in clients:
        if sid != request.sid:
            emit('message', full_msg, to=sid)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in clients:
        del clients[request.sid]

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
