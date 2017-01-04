from flask import request, g
from .. import socketio
import timer

clients = []

@socketio.on("connect")
def on_connect():
    clients.append(request.sid)
    socketio.emit('timer_status', 'active' if timer.timer_active else 'inactive')
    print("Client connected: " + request.sid)


@socketio.on("disconnect")
def on_disconnect():
    clients.remove(request.sid)
    print("Client disconnected: " + request.sid)
