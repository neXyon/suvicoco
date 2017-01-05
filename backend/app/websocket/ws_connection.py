from flask import request, g
from .. import socketio, app
from ..database.SQLiteAccess import get_db
import time


@socketio.on("connect")
def on_connect():
    get_db().cursor().execute("INSERT INTO Connections VALUES (?,?,?)", (request.sid, int(time.time()), True))
    get_db().commit()
    print("Client connected: " + request.sid)


@socketio.on("disconnect")
def on_disconnect():
    get_db().cursor().execute("UPDATE Connections SET is_online = ? WHERE id = ?", (False, request.sid))
    get_db().commit()
    print("Client disconnected: " + request.sid)