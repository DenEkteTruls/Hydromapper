import serial
import pynmea2
import threading

class GPS:

    def __init__(self, nav : object) -> None:

        self.nav = nav
        self.running = True
        
        try:
            self.ser = serial.Serial("/dev/ttyUSB0", 115200)
        except:
            print("[ERROR] Cannot find GPS")


    def start_background_tracking_(self):

        while self.running:
            
            ser = self.ser.readline()
            data = ser.decode()

            items = data.split(",")
            self.nav.GPS = data
            self.nav.position = {'lat': float(items[2]), 'lng': float(items[3])}
            self.nav.heading = float(items[8])
            self.nav.speed = float(items[4])
            self.nav.sats = float(items[1])

        self.running = False


    def start_background_tracking(self):

        threading._start_new_thread(self.start_background_tracking_, ())
