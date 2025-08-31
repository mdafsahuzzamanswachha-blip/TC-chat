from flask import Flask, render_template
from flask_socketio import SocketIO, send
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # Parse JSON string from frontend
    data = json.loads(data)
    msg = data.get("msg")
    nickname = data.get("nickname", "Anonymous")
    image = data.get("image", "")
    
    full_msg = f"{nickname}: {msg}"
    if image:
        full_msg += f" <img src='{image}' style='max-width:200px; display:block;'/>"
    
    send(full_msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
