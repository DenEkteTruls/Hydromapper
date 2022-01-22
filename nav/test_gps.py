import serial
import threading

class GPS:

    def __init__(self) -> None:

        self.running = True
        self.position = {}
        self.heading = None
        self.speed = None
        self.sats = None
        self.GPS = None

        try:
            self.ser = serial.Serial("/dev/ttyUSB0", 115200)
        except:
            print("[ERROR] Cannot find GPS")


    def start_background_tracking(self):

        while self.running:

            ser = self.ser.readline()
            data = ser.decode()

            self.GPS = data

            items = data.split(",")
            self.GPS = data
            self.position = {'lat': float(items[2]), 'lng': float(items[3])}
            self.heading = float(items[8])
            self.speed = float(items[4])
            self.sats = float(items[1])

            print(self.GPS)

        self.running = False

gps = GPS()

gps.start_background_tracking()