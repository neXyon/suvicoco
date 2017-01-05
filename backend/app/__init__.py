from flask import Flask, g
from flask_socketio import SocketIO

socketio = SocketIO()
app = Flask(__name__)

def create_app(debug=False):
    app.debug = debug
    app.config['SECRET_KEY'] = '!suvicoco!'

    socketio.init_app(app)
    return app
