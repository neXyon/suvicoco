import pickle
import os
from datetime import datetime
from threading import Thread, Lock, Condition

class MemoryStorage:
    def __init__(self):
        self.storage = {}

    def store(self, what, when, value):
        if what not in self.storage:
            self.storage[what] = []

        self.storage[what].append((when, value))

class FileStorage(MemoryStorage):
    def __init__(self, directory='/tmp', interval=30):
        super().__init__()
        self.lock = Lock()
        self.namelock = Lock()
        self.callbacklock = Lock()
        self.sleep_condition = Condition()
        self.callbacks = []
        self.changed = False
        self.running = False
        self.thread = None
        self.filename = None
        self.directory = directory
        self.interval = interval

    def subscribe(self, callback):
        with self.callbacklock:
            self.callbacks.append(callback)

    def unsubscribe(self, callback):
        with self.callbacklock:
            self.callbacks.remove(callback)

    def notify(self, what, when, value):
        with self.callbacklock:
            for callback in self.callbacks:
                callback(what, when, value)

    def store(self, what, when, value):
        with self.lock:
            super().store(what, when, value)
            self.changed = True

        Thread(target=self.notify, args=(what, when, value)).start()

    def get(self):
        with self.lock:
            return self.storage.copy()

    def save(self):
        with self.lock:
            if not self.changed:
                return

            self.changed = False

            storage = self.storage.copy()

        with self.namelock:
            with open(self.filename, 'wb') as f:
                pickle.dump(storage, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            storage = pickle.load(f)

        with self.lock:
            self.storage = storage

    def rename(self):
        filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S.pkl')
        filename = os.path.join(self.directory, filename)

        with self.namelock:
            self.filename = filename

    def run(self):
        self.running = True

        while self.running:
            with self.sleep_condition:
                self.sleep_condition.wait(self.interval)

            self.save()

    def start(self):
        self.rename()

        if self.running:
            return

        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False

        if self.thread:
            with self.sleep_condition:
                self.sleep_condition.notify()
            self.thread.join()
            self.thread = None
