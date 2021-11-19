import os
import numpy as np

class Rudder:

    def __init__(self, pin, pi):

        self.pi = pi
        self.pin = pin
        self.right = 600
        self.mid = 1050
        self.left = 1500

        self.degrees = np.linspace(self.right, self.left, 122)


    def set_heading(self, heading : int) -> None:

        hz = self.degrees[heading+60]
        self.pi.set_servo_pulsewidth(self.esc_pin, hz)