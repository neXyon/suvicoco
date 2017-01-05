from .. import socketio
from ..database.SQLiteAccess import get_db

@socketio.on('cooking_action')
def cooking(data):
    if data['cmd'] == 'start':
        if 'temp' in data:
            print("Start cooking with " + str(data['temp']) + "°C")
            startCooking()
        else:
            print("No temperature given... ")


def startCooking():
    pass