from flask import Flask, request
from flask_socketio import SocketIO
from .simulation import SimulatorInterface
from .hardware import ElectronicsInterface
from .storage import FileStorage
from .control import CookerController

import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

class App:
    def __init__(self, debug=False):
        self.storage = FileStorage()

        if debug:
            self.interface = SimulatorInterface(time_factor=1.0)
        else:
            self.interface = ElectronicsInterface()

        self.controller = CookerController(self.interface, self.storage)

        self.flask = Flask(__name__)
        self.sio = SocketIO()

        self.flask.debug = debug
        self.flask.config['SECRET_KEY'] = '!suvicoco!'

        self.sio.init_app(self.flask)

        self.storage.subscribe(self.storage_callback)
        self.controller.subscribe(self.stop_callback)

        self.status = False

    def get_data(self):
        return self.storage.get()

    def get_status(self):
        return self.status

    def start(self):
        self.sio.run(self.flask, use_reloader=False)

    def stop_callback(self):
        self.storage.stop()
        self.status = False
        self.sio.emit('stopped')

    def storage_callback(self, what, when, value):
        print("Storage", what, when, value)
        self.sio.emit('update', json.dumps({'what': what, 'when': when, 'value': value}, cls=DateTimeEncoder))

    def start_cooking(self, target_temperature):
        self.storage.start()
        self.controller.set_target(target_temperature)
        self.controller.start()
        self.sio.emit('start', json.dumps({'temperature': target_temperature}))
        self.status = True

    def stop_cooking(self):
        self.controller.stop()

    def set_temperature(self, target_temperature):
        self.controller.set_target(target_temperature)
        self.sio.emit('temperature', json.dumps({'temperature': target_temperature}))

app = App(True)

#@app.sio.on("connect")
#def on_connect():
#    print("Client connected: " + request.sid)

#@app.sio.on("disconnect")
#def on_disconnect():
#    print("Client disconnected: " + request.sid)

@app.sio.on('start cooking')
def start_cooking(json):
    print(json)
    if 'temperature' in json:
        try:
            temperature = float(json['temperature'])
        except ValueError:
            return
        app.start_cooking(temperature)
        print("Started cooking")

@app.sio.on('stop cooking')
def stop_cooking(json):
    app.stop_cooking()
    print("Stopped cooking")

@app.sio.on('set temperature')
def set_temperature(json):
    if 'temperature' in json:
        try:
            temperature = float(json['temperature'])
        except ValueError:
            return
        app.set_temperature(temperature)

@app.sio.on('get data')
def get_data(data):
    data = app.get_data()
    emit('data', json.dumps(data, cls=DateTimeEncoder))

@app.sio.on('get status')
def get_status(data):
    data = app.get_status()
    emit('status', json.dumps(data))
