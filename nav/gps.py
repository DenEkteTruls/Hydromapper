import serial
import pynmea2
import threading

class GPS:

    def __init__(self, nav : object) -> None:

        self.nav = nav
        self.running = True
        self.last_position = {}
        
        try:
            self.ser = serial.Serial("/dev/ttyS0", 9600)
        except:
            print("[ERROR] Cannot find GPS")


    def start_background_tracking_(self):

        while self.running:
            
            ser = self.ser.readline() 
            data = ser.decode()

            if "GNGGA" in data.split(",")[0]:
                try:
                    s = data.split(",")
                    self.nav.position = {'lat': float(s[2])/100 + 0.193328, 'lng': float(s[4])/100 + 0.12404}
                    self.nav.sats = float(s[7])
                    self.GPS = pynmea2.parse(data)
                except:
                    pass

            elif "VTG" in data.split(",")[0]:
                s = data.split(",")

                try:self.nav.speed = float(s[5])
                except: pass

                if not self.last_position == {}:
                    self.nav.course = self.nav.get_heading(self.nav.position, self.last_position)

                self.last_position = self.nav.position

        self.running = False


    def start_background_tracking(self):

        threading._start_new_thread(self.start_background_tracking_, ())
