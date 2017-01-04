import time
from threading import Thread
from flask import g
from .. import socketio

start_time = -1
elapsed_time = 0

timer_active = False

@socketio.on('timer_action')
def timer(data):
    if data == 'start':
        start_timer()
    elif data == 'stop':
        stop_timer()


def start_timer():
    global timer_active
    global start_time

    if timer_active:
        return

    start_time = time.time()
    timer_active = True
    t = Thread(target=send_elapsed_time)
    t.setDaemon(True)
    t.start()

    socketio.emit('timer_status', 'active')

    print("Timer started")


def stop_timer():
    global timer_active
    global start_time
    global elapsed_time

    if not timer_active:
        return

    start_time = -1
    timer_active = False
    print("Timer stopped: " + str(int(elapsed_time)))
    socketio.emit('timer_status', 'inactive')
    return int(elapsed_time)


def send_elapsed_time():
    global timer_active
    global elapsed_time
    global start_time

    while(timer_active):
        elapsed_time = time.time() - start_time
        #print('Time elapsed: ' + str(int(elapsed_time)))
        socketio.emit('timer_elapsed', int(elapsed_time))
        time.sleep(0.1)
