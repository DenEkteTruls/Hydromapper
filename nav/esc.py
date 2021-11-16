import os
import numpy as np


class ESC:

    idx = -1

    def __init__(self, esc_pin):

        self.id = ESC.idx + 1; ESC.ids = self.id
        self.esc_pin = esc_pin
        self.speed = 0


    def report(self, message : str) -> None:

        print(f"[ESC] {message}")

    
    def set_speed__(self, speed : int):

        speed_ = (speed * 10) + 1000

        os.system(f"pigs s {self.esc_pin} {int(speed_)}")
        self.report(f"Speed change -> {speed}")


    def arm(self):

        self.report("ARMING ...")
        self.set_speed__(0)
        self.report("ARMED")

    
    def set(self, speed):

        self.set_speed__(speed)
        

    def disarm(self):

        self.report("DISARMING ...")
        os.system(f"pigs s {self.esc_pin} 0")
        self.report("DISARMED")