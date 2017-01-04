from flask import request, g
from .. import socketio

clients = []

@socketio.on("connect")
def on_connect():
    clients.append(request.sid)
    print("Client connected: " + request.sid)


@socketio.on("disconnect")
def on_disconnect():
    clients.remove(request.sid)
    print("Client disconnected: " + request.sid)
