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
                s = data.split(",")
                self.nav.position = {'lat': float(s[2])/100 + 0.193328, 'lng': float(s[4])/100 + 0.12404}
                self.nav.sats = float(s[7])
                self.GPS = pynmea2.parse(data)

            elif "VTG" in data.split(",")[0]:
                s = data.split(",")
                self.nav.speed = float(s[5])
                self.nav.GPScompass = float(s[1])
            """
            try:
                msg = pynmea2.parse(ser.decode()); msg.num_sats
#                x, y = utm.from_latlon(float(msg.lat)/100, float(msg.lon)/100)[0:2]
                position = {'lat': float(msg.lat)/100, 'lng': float(msg.lon)/100}

                if self.last_position == {}:
                    pass
                else:
                    self.nav.GPScompass = self.nav.get_heading(self.last_position, position)

                self.nav.position = position
                self.nav.GPS = msg
                self.nav.sats = msg.num_sats

                self.last_position = position
            except:
                pass
            """

        self.running = False


    def start_background_tracking(self):

        threading._start_new_thread(self.start_background_tracking_, ())
