from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")  # ⚠️ important

clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    clients[request.sid] = "Anonymous"
    print(f"{request.sid} connected")  # debug

@socketio.on('set_nickname')
def set_nickname(nickname):
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

    # send message to all clients including sender
    for sid in clients:
        emit('message', full_msg, to=sid)

@socketio.on('disconnect')
def disconnect():
    if request.sid in clients:
        del clients[request.sid]

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
