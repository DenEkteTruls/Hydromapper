import os
import numpy as np
        
class Rudder:
        
    def __init__(self, pin, nav, pi):
        
        self.pi = pi
        self.pin = pin
        self.right = 600
        self.mid = 1134
        self.left = 1800
        
        self.degrees = np.linspace(self.right, self.mid, 60).tolist() + np.linspace(self.mid, self.left, 60).tolist()
        
        for i, d in enumerate(self.degrees):
            self.degrees[i] = int(round(d, 0))
        
        
    def set_heading(self, heading : int) -> None:
        
        hz = self.degrees[heading+59]
        self.pi.set_servo_pulsewidth(self.pin, hz)
