#!/bin/env python
from app import create_app, socketio
import app.websocket
import app.database
import sys
import signal

app = create_app(debug=False)

if __name__ == "__main__":
    print("\tServing HTTP and WEBSOCKET on http://localhost:5000")
    socketio.run(app)
    signal.signal(signal.SIGINT, signal_handler)

def signal_handler(signal, frame):
    sys.exit(0)
