from flask import Flask, request
from flask_socketio import SocketIO

clients = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def index():
    return "INDEX"

@socketio.on("connect")
def on_connect():
    clients.append(request.sid)
    print("Client connected: " + request.sid)

@socketio.on("disconnect")
def on_disconnect():
    clients.remove(request.sid)
    print("Client disconnected: " + request.sid)

if __name__ == "__main__":
    print("\tServing HTTP and WEBSOCKET on http://localhost:5000")
    socketio.run(app)
