import numpy as np
import datetime

class WaterHeaterModel:
    def __init__(self, m_w=1, m_h=0.2, T_env=23, P=400, r=0.085,
                 c_pw=4200, c_ph=400, h_w=25, h_a=6, rho_w=1000, rho_h=8800):
        A_hw = np.pi * r ** 2
        V_w = m_w / rho_w
        H_w = V_w / A_hw
        A_wa = H_w * 2 * r * np.pi + A_hw

        V_h = m_h / rho_h
        H_h = V_h / A_hw
        A_ha = H_h * 2 * r * np.pi + A_hw

        alpha = -(h_w * A_hw + h_a * A_ha) / (c_ph * m_h)
        beta = h_w * A_hw / (c_ph * m_h)
        gamma = h_w * A_hw / (c_pw * m_w)
        delta = -(h_w * A_hw + h_a * A_wa) / (c_pw * m_w)

        self.A = np.array([[alpha, beta], [gamma, delta]])

        alpha = P / (c_ph * m_h)
        beta = h_a * A_ha / (c_ph * m_h) * T_env
        gamma = 0
        delta = h_a * A_wa / (c_pw * m_w) * T_env

        self.B = np.array([[alpha, beta], [gamma, delta]])

        self.state = np.array([[T_env] * 2], dtype=np.float64).transpose()

    def __call__(self, u, dt):
        u = np.array([[u, 1]]).transpose()

        self.state += (np.dot(self.A, self.state) + np.dot(self.B, u)) * dt

        return self.state

class SimulatorInterface:
    def __init__(self, m=None, time_base=datetime.datetime.now, time_factor=1.0, switching_delay=5.0, accuracy=0.125):
        if m is None:
            m = np.random.rand() + 0.7

        self.model = WaterHeaterModel(m)
        self.heating = False
        self.time_base = time_base
        self.last_time = time_base()
        self.time_factor = time_factor
        self.switching_delay = switching_delay
        self.accuracy = accuracy
        self.last_temperature = np.random.rand() * 80 + 20
        self.relays = []

    def _update(self):
        current = self.time_base()
        dt = (current - self.last_time).total_seconds() * self.time_factor
        self.advance(dt, current)

    def advance(self, dt, current=None):
        if current is None:
            current = self.time_base()
        self.last_time = current

        self.relays = [(x[0] - dt, x[1]) for x in self.relays]

        while len(self.relays) > 0 and self.relays[0][0] <= 0:
            self.heating = self.relays[0][1]
            self.relays = self.relays[1:]

        self.model(float(self.heating), dt)

    def read_temperature(self):
        # note: ugly delay like we have in the actual sensor readings
        result = np.round(self.last_temperature / self.accuracy + np.random.randn(1)[0] / 3) * self.accuracy
        self._update()
        self.last_temperature = self.model.state[1][0]
        return result

    def write_relay(self, value):
        self._update()
        self.relays.append((self.switching_delay, value))

    def close(self):
        pass
