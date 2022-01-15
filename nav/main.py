import time
import pynmea2
from nav import Nav
from esc import ESC
from rudder import Rudder
from networking import Networking
from sonar import Sonar
from gps import GPS

nav = Nav()
sonar = Sonar(nav = nav)
gps = GPS(nav = nav)
esc = ESC(esc_pin = 18)
rudder = Rudder(pin = 17, nav = nav, pi = esc.pi)
net = Networking("192.168.10.106", 8081, 1024)
gps.start_background_tracking()
sonar.run_in_background()

nav.add_esc(esc)
nav.add_rudder(rudder)
nav.load_waypoints("waypoints.json")
net.listener()

nav.show_simulated_route()
nav.start_autopilot()

while nav.running or nav.retHome:
    
<<<<<<< HEAD
    print(f"HEADING: {nav.GPScompass}\tOFFSET: {nav.offset}\tSPEED: {nav.depth}\tPOSITION: {nav.position}")
=======
    #print(f"HEADING: {nav.GPScompass}\tOFFSET: {nav.offset}\tSPEED: {nav.depth}\tPOSITION: {nav.position}")
    #print(nav.GPS)
>>>>>>> f2969589f1270a4520c1911872d81ff81ad39379

    if not nav.handle_networking(net.recieved):
        nav.running = False
        net.running = False
        sonar.running = False
        gps.running = False
    time.sleep(0.5)

exit()
