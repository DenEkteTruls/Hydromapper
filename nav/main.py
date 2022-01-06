from nav import Nav
from esc import ESC
from rudder import Rudder
from networking import Networking
from sonar import Sonar
from gps import GPS
import pigpio
import time
import pynmea2

pi = pigpio.pi()
nav = Nav()
sonar = Sonar(nav = nav)
gps = GPS(nav = nav)
esc = ESC(esc_pin = 4, pi = pi)
rudder = Rudder(pin = 17, nav = nav, pi = pi)
net = Networking("192.168.10.106", 8081, 1024)
gps.start_background_tracking()
sonar.run_in_background()

nav.add_esc(esc)
nav.add_rudder(rudder)
nav.load_waypoints("waypoints.json")
net.listener()

while nav.running or nav.retHome:
    
#    print(nav.depth)
#    print(nav.position)
    print(nav.GPScompass)

    if not nav.handle_networking(net.recieved):
        nav.running = False
        net.running = False
        sonar.running = False
        gps.running = False
    time.sleep(0.5)

exit()
