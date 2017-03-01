from flask import Flask, request
from flask_socketio import SocketIO
from .simulation import SimulatorInterface
from .hardware import ElectronicsInterface
from .storage import FileStorage
from .control import CookerController

from flask import json

def stop_callback():
    global status, storage, socketio
    storage.stop()
    status = False
    socketio.emit('stopped')

def storage_callback(what, when, value):
    global socketio
    print("Storage", what, when, value)
    socketio.emit('update', {'what': what, 'when': when, 'value': value})

debug = True

app = Flask(__name__)
app.debug = debug
app.config['SECRET_KEY'] = '!suvicoco!'
socketio = SocketIO(app, async_mode='threading', json=json)

storage = FileStorage(thread_starter=socketio.start_background_task)

if debug:
    interface = SimulatorInterface(time_factor=1.0)
else:
    interface = ElectronicsInterface()

controller = CookerController(interface, storage, socketio.start_background_task)

storage.subscribe(storage_callback)
controller.subscribe(stop_callback)

status = False

#@socketio.on("connect")
#def on_connect():
#    print("Client connected: " + request.sid)

#@socketio.on("disconnect")
#def on_disconnect():
#    print("Client disconnected: " + request.sid)

@app.route('/control/start/<float:temperature>')
@app.route('/control/start/<int:temperature>')
def start_cooking(temperature):
    global storage, controller, status, socketio

    if temperature < 40 or temperature > 95:
        return json.dumps('false')


    storage.start()
    controller.set_target(temperature)
    controller.start()
    socketio.emit('started', {'temperature': temperature})
    status = True
    print("Started cooking")

    return 'true'

@app.route('/control/stop')
def stop_cooking():
    global controller

    controller.stop()
    print("Stopped cooking")

    return 'true'

@app.route('/control/set/<float:temperature>')
def set_temperature(temperature):
    global controller, socketio

    if temperature < 40 or temperature > 95:
        return 'false'

    controller.set_target(temperature)
    socketio.emit('temperature', {'temperature': temperature})

    return 'true'

@app.route('/control/data')
def get_data():
    data = json.dumps(storage.get())
    return data

@app.route('/control/status')
def get_status():
    return json.dumps(status)
