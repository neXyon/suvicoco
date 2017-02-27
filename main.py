import sys
import signal
from suvicoco.app import socketio

#def signal_handler(signal, frame):
#    sys.exit(0)

if __name__ == "__main__":
    #print("\tServing HTTP and WEBSOCKET on http://localhost:5000")
    #signal.signal(signal.SIGINT, signal_handler)
    socketio.run(app)#, use_reloader=False)
