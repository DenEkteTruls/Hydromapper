import os
import numpy as np

class Rudder:

    def __init__(self, pin):

        self.pin = pin
        self.right = 600
        self.mid = 1050
        self.left = 1500

        self.degrees = np.linspace(self.right-2, self.left+2, 120)


    def set_heading(self, heading : int) -> None:

        hz = self.degrees[heading+59]
        os.system(f"pigs s {self.pin} {hz}")