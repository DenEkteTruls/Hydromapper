import serial
import threading

class GPS:

    def __init__(self, nav : object) -> None:

        self.nav = nav
        self.running = True
        self.GPS = None
        self.last_pos = {}
        
        try:
            self.ser = serial.Serial("/dev/ttyUSB0", 115200)
        except:
            print("[ERROR] Cannot find GPS")


    def start_background_tracking_(self):

        while self.running:
            
            ser = self.ser.readline()
            data = ser.decode()

            self.GPS = data

            items = data.split(",")
            if len(items) > 0:
                self.nav.GPS = data

                try: self.nav.position = {'lat': float(items[2]), 'lng': float(items[3])}
                except: self.nav.position = {'lat': 0, 'lng': 0}

                try: self.nav.speed = float(items[4])
                except: self.nav.speed = -1

                #try:
                    #a = float(items[8]) + 90
                    #if a > 360: a -= 360
                    #self.nav.heading = a
                #except: self.nav.heading = -1

                try: self.nav.sats = float(items[1])
                except: self.nav.sats = -1

                if not self.last_pos == {}:
                    self.nav.heading = self.nav.get_heading(self.nav.position, self.last_pos);

                self.last_pos  = self.nav.position

        self.running = False


    def start_background_tracking(self):

        threading._start_new_thread(self.start_background_tracking_, ())
