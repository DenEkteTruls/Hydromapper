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
<<<<<<< HEAD
        self.pi.set_servo_pulsewidth(self.esc_pin, hz)
=======
        self.pi.set_servo_pulsewidth(self.esc_pin, hz)
>>>>>>> 11f069ab5561c57589a37982f705b16dda88416f
