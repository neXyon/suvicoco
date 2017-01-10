from flask import request
from .. import socketio, app
from ..database import Connection

@socketio.on("connect")
def on_connect():
    Connection.add_connection(request.sid)
    print("Client connected: " + request.sid)


@socketio.on("disconnect")
def on_disconnect():
    Connection.close_connection(request.sid)
    print("Client disconnected: " + request.sid)


@app.route("/connections/current")
def current_connections():
    return str(Connection.get_current_connections())

