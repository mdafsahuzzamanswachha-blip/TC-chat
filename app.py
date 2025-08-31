import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    clients[request.sid] = "Anonymous"

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
        full_msg += f"<br/><img src='{image}' style='max-width:200px; display:block;margin-top:5px;border-radius:10px;'/>"

    for sid in clients:
        emit('message', full_msg, to=sid)

@socketio.on('disconnect')
def disconnect():
    if request.sid in clients:
        del clients[request.sid]

# WebRTC signaling
@socketio.on("webrtc_offer")
def webrtc_offer(offer):
    emit("webrtc_offer", offer, broadcast=True, include_self=False)

@socketio.on("webrtc_answer")
def webrtc_answer(answer):
    emit("webrtc_answer", answer, broadcast=True, include_self=False)

@socketio.on("webrtc_ice_candidate")
def webrtc_ice(candidate):
    emit("webrtc_ice_candidate", candidate, broadcast=True, include_self=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
