import numpy as np
import time
import datetime
import os
import threading
from enum import Enum
from .util import startThread

class CookerController:
    class States(Enum):
        BOOST = 1
        OVERSHOOT = 2
        CONTROL = 3
        STOPPED = 4

    CONTROL_EPSILON = 0.5
    F_SWITCH = 1 / 15
    T_CONT = 2 / F_SWITCH
    F_READ = 1
    T_READ = 1 / F_READ
    N_CONTROL = int(T_CONT / T_READ)
    NE_CONTROL = 4

    NM_CONTROL = 3
    NC_CONTROL = 4

    CONTROL_MIN_CHANGE_TIME = 5 * 60 // N_CONTROL

    TARGET_ACCURACY = 0.2
    MAXIMUM_CONTROL_ERROR = 1.0
    BOOST_COOL_SAMPLES = 30
    MIN_BOOST_DURATION_FOR_V_UPDATE = 30
    MAX_V_BOOST = 20
    MIN_V_BOOST = 10

    MAX_BOOST_FAILURES = 3
    MAX_OVERSHOOT_TIME = 60 * 60 # 60 mins
    MAX_TEMPERATURE = 98
    MAX_RUNTIME = 48 * 60 * 60 # 48 hours

    LID_OPEN_MAX_TIME = 30
    LID_OPEN_MIN_CHANGE = 1

    def __init__(self, interface, storage=None, thread_starter=startThread):
        self.time_factor = 1
        self.interface = interface
        self.storage = storage
        self.thread_starter = thread_starter

        self.lock = threading.Lock()
        self.callbacks = []

        self.thread = None

        self.reset()

    def subscribe(self, callback):
        with self.lock:
            self.callbacks.append(callback)

    def unsubscribe(self, callback):
        with self.lock:
            self.callbacks.remove(callback)

    def notify(self):
        with self.lock:
            for callback in self.callbacks:
                callback()

    def reset(self):
        self.now = datetime.datetime.now()

        self.state = CookerController.States.STOPPED
        self.relay_on = False

        self.running = False

        self.v_boost = 15

        self.current_mean = 0

        self.set_target(40, False)

        self.control_a = 0.1
        self.control_n = 0
        self.control_means = []

        self.control_cycle_state = 0

        self.control_applied_change = False
        self.control_last_change = 0

        self.control_turnoff = 0

        self.start_state = True

        self.boost_time = 0
        self.boost_cool = 0
        self.boost_heat = 0
        self.boost_samples = 0
        self.boost_start = 0
        self.boost_failures = 0

        self.overshoot_start = None

        self.lid_open = False
        self.lid_open_start = self.now

        self.stop_reason = "Reset"

    def start(self):
        if self.running:
            return

        if self.thread:
            self.thread.join()

        self.thread = self.thread_starter(self.run)

    def run(self):
        self.running = True

        # read once to trigger temperature sensor readings (aka first reading might be outdated)
        self.interface.read_temperature()

        self.relay_on = False
        self.interface.write_relay(False)

        self.switch_state(CookerController.States.OVERSHOOT)

        self.iteration = 0
        self.start_time = datetime.datetime.now()
        self.handling_temps = []
        self.now = datetime.datetime.now()

        if self.storage:
            self.storage.store('v_boost', self.now, self.v_boost)

        while(self.running):
            self.timestep()

        if self.relay_on:
            self.interface.write_relay(False)
            self.relay_on = False

        self.switch_state(CookerController.States.STOPPED)

        self.thread_starter(self.notify)

    def stop(self):
        self.running = False
        self.stop_reason = "Manual"
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def set_target(self, value, store=True):
        # TODO: consider changes while cooking?!
        self.target_temperature = value

        self.control_last_min = self.target_temperature - CookerController.MAXIMUM_CONTROL_ERROR
        self.control_last_max = self.target_temperature + CookerController.MAXIMUM_CONTROL_ERROR

        self.control_max = 0.07
        self.control_min = 0.02

        if self.storage and store:
            self.storage.store('target_temperature', self.now, self.target_temperature)
            self.storage.store('control_min', self.now, self.control_min)
            self.storage.store('control_max', self.now, self.control_max)

    def set_control_a(self, value, state=None):
        self.control_a = value

        if self.storage:
            self.storage.store('control_a', self.now, value)

        if state is not None:
            self.control_cycle_state = state

            if self.storage:
                self.storage.store('control_cycle_state', self.now, self.control_cycle_state)

    def security(self):
        # file controlled emergency stop
        if os.path.exists('/tmp/stop'):
            self.stop_reason = "External Stop"
            return True

        # heating results in no temperature change
        if self.boost_failures >= CookerController.MAX_BOOST_FAILURES:
            self.stop_reason = "Heating not effective"
            return True

        # overshooting too much and/or temperature not going down
        if self.overshoot_start is not None and ((self.now - self.overshoot_start).total_seconds() * self.time_factor >= CookerController.MAX_OVERSHOOT_TIME):
            self.stop_reason = "Overshooting too much"
            return True

        # maximum temperature
        if self.temperature > CookerController.MAX_TEMPERATURE:
            self.stop_reason = "Maximum temperature"
            return True

        # maximum operation time
        if (self.now - self.start_time).total_seconds() * self.time_factor >= CookerController.MAX_RUNTIME:
            self.stop_reason = "Maximum operation time"
            return True

        return False

    def lid_check(self):
        handling_temp = self.temperature

        if self.lid_open:
            if self.handling_temps[-1] - self.temperature < CookerController.LID_OPEN_MIN_CHANGE or ((self.now - self.lid_open_start).total_seconds() * self.time_factor >= CookerController.LID_OPEN_MAX_TIME):
                self.lid_open = False

                if self.storage:
                    self.storage.store('lid_open', self.now, self.lid_open)
            else:
                handling_temp = self.handling_temps[-1]
        elif self.handling_temps and (self.handling_temps[-1] - self.temperature > CookerController.LID_OPEN_MIN_CHANGE):
            self.lid_open = True
            self.lid_open_start = self.now
            handling_temp = self.handling_temps[-1]

            if self.storage:
                self.storage.store('lid_open', self.now, self.lid_open)

        self.handling_temps.append(handling_temp)

    def timestep(self):
        self.iteration += 1
        self.last_time = self.now
        self.now = datetime.datetime.now()

        self.temperature = self.interface.read_temperature()

        if self.storage:
            self.storage.store('temperature', self.now, self.temperature)

        self.lid_check()

        # delta time
        self.dt = (self.now - self.last_time).total_seconds() * self.time_factor

        if self.control_turnoff > 0:
            self.control_turnoff -= self.dt
        if self.boost_time > 0:
            self.boost_time -= self.dt

        self.relay_target = self.relay_on

        # state routines
        if self.state == CookerController.States.CONTROL:
            self.control()
        elif self.state == CookerController.States.BOOST:
            self.boost()
        elif self.state == CookerController.States.OVERSHOOT:
            self.overshoot()
        else:
            self.stop_reason = "Invalid state"
            self.running = False
            return

        # actually switch the relay!
        if self.relay_on != self.relay_target:
            self.relay_on = self.relay_target
            self.interface.write_relay(self.relay_on)

            if self.storage:
                self.storage.store('relay', self.now, self.relay_on)

        emergency_stop = self.security()

        if emergency_stop:
            self.running = False
            return

        # sleep time
        sleep_time = self.iteration + 1 - (datetime.datetime.now() - self.start_time).total_seconds() * self.time_factor

        # precise relay control for control
        if self.state == CookerController.States.CONTROL and self.relay_on and sleep_time > self.control_turnoff:
            if self.control_turnoff > 0:
                time.sleep(self.control_turnoff / self.time_factor)
                sleep_time -= self.control_turnoff
            self.control_turnoff = 0
            self.relay_on = False
            self.interface.write_relay(self.relay_on)

            if self.storage:
                self.storage.store('relay', self.now, self.relay_on)

        if sleep_time > 0:
            time.sleep(sleep_time / self.time_factor)

    def switch_state(self, state):
        self.state = state
        self.start_state = True
        if self.storage:
            self.storage.store('state', self.now, self.state.value)

    def control(self):
        self.control_n += 1

        if self.start_state:
            self.control_n = 0
            self.control_means = []

            self.control_cycle_state = 0

            if self.storage:
                self.storage.store('control_cycle_state', self.now, self.control_cycle_state)

            self.control_last_change = 0
            self.control_applied_change = False

            self.start_state = False

        # control period is over
        if self.control_n == CookerController.N_CONTROL:
            self.control_last_change += 1

            self.control_n = 0

            self.current_mean = np.mean(self.handling_temps[-CookerController.N_CONTROL:])

            # mean temperature in last control period
            self.control_means.append(self.current_mean)

            if self.storage:
                self.storage.store('control_cycle_mean', self.now, self.current_mean)

            # mean temperature was higher than target
            if self.current_mean > self.target_temperature:
                if self.control_cycle_state == 0:
                    # cycle just started, we start controlling with the minimum
                    self.set_control_a(self.control_min, 1)
                elif self.control_cycle_state == 2:
                    # cycle is over

                    # if the difference between min and max is big enough adapt!
                    if self.control_max - self.control_min > 0.01:
                        if np.mean(self.control_means) > self.target_temperature:
                            # on average we were higher than the target -> lower the max
                            self.control_max -= 0.25 * (self.control_max - self.control_min)
                            if self.storage:
                                self.storage.store('control_max', self.now, self.control_max)
                        else:
                            # on average we were lower than the target -> increase the min
                            self.control_min += 0.25 * (self.control_max - self.control_min)
                            if self.storage:
                                self.storage.store('control_min', self.now, self.control_min)

                    self.set_control_a(self.control_min, 1)

                    self.control_last_min = np.min(self.control_means)
                    self.control_last_max = np.max(self.control_means)

                    self.control_applied_change = False

                    self.control_means = []
                elif self.current_mean > self.control_last_max and (not self.control_applied_change or self.control_last_change >= CookerController.CONTROL_MIN_CHANGE_TIME):
                    # temperature is bigger than last max - probably increased the min too much
                    self.control_min -= 0.25 * (self.control_max - self.control_min)

                    if self.storage:
                        self.storage.store('control_min', self.now, self.control_min)

                    self.set_control_a(self.control_min)
                    self.control_applied_change = True
                    self.control_last_change = 0

            elif self.current_mean < self.target_temperature:
                if self.control_cycle_state == 1:
                    # wait for cycling up again
                    self.set_control_a(self.control_max, 2)
                    self.control_applied_change = False
                elif self.current_mean < self.control_last_min and (not self.control_applied_change or self.control_last_change >= CookerController.CONTROL_MIN_CHANGE_TIME):
                    # temperature is lower than last min - probably decreased max too much
                    self.control_max += 0.25 * (self.control_max - self.control_min)

                    if self.storage:
                        self.storage.store('control_max', self.now, self.control_max)

                    self.set_control_a(self.control_max)
                    self.control_applied_change = True
                    self.control_last_change = 0

            # state switches
            if self.current_mean > self.target_temperature + CookerController.MAXIMUM_CONTROL_ERROR:
                self.control_max /= 2
                self.control_min /= 2

                if self.storage:
                    self.storage.store('control_min', self.now, self.control_min)


                self.switch_state(CookerController.States.OVERSHOOT)

            elif self.current_mean < self.target_temperature - CookerController.MAXIMUM_CONTROL_ERROR:
                self.switch_state(CookerController.States.BOOST)

                self.control_max *= 1.5

                if self.storage:
                    self.storage.store('control_max', self.now, self.control_max)


        # turn relay on
        if self.control_n == 0 and self.state == CookerController.States.CONTROL:
            self.control_turnoff = self.control_a * CookerController.T_CONT

            if self.control_turnoff > 0:
                self.relay_target = True

    def boost(self):
        if self.start_state:
            self.boost_start = self.handling_temps[-1]
            dT = self.target_temperature - self.boost_start
            self.boost_time = self.v_boost * dT
            self.boost_heat = self.boost_time
            self.boost_samples = 0

            self.relay_target = True
            self.start_state = False
        else:
            self.boost_samples += 1

        if self.boost_time <= 0:
            if self.relay_on:
                self.relay_target = False
                self.boost_heat -= self.boost_time
                self.boost_cool = 0
            else:
                self.boost_cool += self.dt

                if self.boost_cool > CookerController.BOOST_COOL_SAMPLES:
                    if np.mean(np.array(self.handling_temps[-CookerController.BOOST_COOL_SAMPLES - 1:-1]) - np.array(self.handling_temps[-CookerController.BOOST_COOL_SAMPLES:])) > 0:

                        max_temp = np.max(self.handling_temps[-self.boost_samples:])
                        # TODO: what if it didn't heat yet, but temperature decreased during "cooling"
                        #    - doing nothing will boost the same amount again, which prob. is fine...

                        if self.boost_heat > CookerController.MIN_BOOST_DURATION_FOR_V_UPDATE and max_temp > self.boost_start:
                            self.v_boost = np.max([np.min([self.boost_heat / (max_temp - self.boost_start), CookerController.MAX_V_BOOST]), CookerController.MIN_V_BOOST])

                            if self.storage:
                                self.storage.store('v_boost', self.now, self.v_boost)

                        if max_temp <= self.boost_start:
                            self.boost_failures += 1
                        else:
                            self.boost_failures = 0

                        # state switch
                        if self.handling_temps[-1] > self.target_temperature:
                            self.switch_state(CookerController.States.OVERSHOOT)
                        elif self.handling_temps[-1] > self.target_temperature - CookerController.CONTROL_EPSILON:
                            self.switch_state(CookerController.States.CONTROL)
                        else:
                            self.start_state = True

        # overshooting, stop heating early!
        elif self.relay_on and self.handling_temps[-1] >= self.target_temperature:
            self.relay_target = False
            self.boost_heat -= self.boost_time
            self.boost_time = 0
            self.boost_cool = 0

    def overshoot(self):
        if self.start_state:
            self.overshoot_start = self.now
            self.start_state = False
            self.relay_target = False

        if self.handling_temps[-1] < self.target_temperature - CookerController.CONTROL_EPSILON:
            self.overshoot_start = None
            self.switch_state(CookerController.States.BOOST)
        elif self.handling_temps[-1] < self.target_temperature:
            self.overshoot_start = None
            self.switch_state(CookerController.States.CONTROL)
