import os
import pigpio
import numpy as np


class ESC:

    idx = -1

    def __init__(self, esc_pin):

        self.pi = pigpio.pi()
        self.id = ESC.idx + 1; ESC.ids = self.id
        self.esc_pin = esc_pin
        self.speed = 0

        os.system("sudo pigpiod")


    def report(self, message : str) -> None:

        print(f"[ESC] {message}")

    
    def set_speed__(self, speed : int):

        self.speed = 16 + speed
        self.pi.set_PWM_dutycycle(self.esc_pin, self.speed)
        print(f"[MOTOR] Speed change -> {self.speed}")


    def arm(self):

        self.report("ARMING ...")
        self.set_speed__(0)
        self.report("ARMED")

    
    def set(self, speed):

        self.set_speed__(int(speed))
        

    def disarm(self):

        self.report("DISARMING ...")
        self.set_speed__(0)
        self.report("DISARMED")
