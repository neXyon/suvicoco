import numpy as np
import glob
from .util import *

class ElectronicsInterface:
    def __init__(self, gpio_pin=18, sensor=None):
        self.pin = gpio_pin
        self.sensor = None
        self.GPIO = None

        if sensor is None:
            temperature_sensors = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')

            if len(temperature_sensors) > 1:
                printError('multiple temperature sensors found, please specify - entering fake mode')
                return
            elif len(temperature_sensors) == 0:
                printError('temperature sensor cannot be found - entering fake mode')
                return
            else:
                printDebug('temperature sensor found: ' + temperature_sensors[0])
                sensor = temperature_sensors[0]

        self.sensor = sensor

        try:
            self.read_temperature()
        except:
            printError('temperature sensor cannot be read - entering fake mode.')
            self.sensor = None
            return

        try:
            import RPi.GPIO as GPIO

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(gpio_pin, GPIO.OUT, initial=GPIO.LOW)

            self.GPIO = GPIO

            printDebug('GPIO up and running')
        except:
            self.GPIO = None
            printError('GPIO not working - entering fake mode')

    def read_temperature(self):
        if self.sensor is not None:
            with open(self.sensor, 'r') as f:
                lines = f.readlines()
        else:
            lines = ['69 01 ff ff 7f ff ff ff 7e : crc=7e YES\n', '69 01 ff ff 7f ff ff ff 7e t=22562\n']

        if lines[0].strip()[-3:] == 'YES':
            self.temperature = int(lines[1].strip().split('=')[1]) / 1000
        else:
            self.temperature = np.nan
            printWarning('no temperature read')

        return self.temperature

    def write_relay(self, value):
        if self.GPIO is not None:
            self.GPIO.output(self.pin, value)

    def close(self):
        if self.GPIO is not None:
            self.GPIO.cleanup(self.pin)
