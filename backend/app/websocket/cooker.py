from .. import socketio


@socketio.on('cooking_action')
def cooking(data):
    if data['cmd'] == 'start':
        if 'temp' in data:
            print("Start cooking with " + str(data['temp']) + "°C")
        else:
            print("No temperature given... ")

