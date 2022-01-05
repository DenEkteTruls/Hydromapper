from nav import Nav
from esc import ESC
from rudder import Rudder
from networking import Networking
from sonar import Sonar
import pigpio
import time

pi = pigpio.pi()
nav = Nav()
sonar = Sonar(nav = nav)
esc = ESC(esc_pin = 4, pi = pi)
rudder = Rudder(pin = 17, pi = pi)
net = Networking("localhost", 8081, 1024)

nav.add_esc(esc)
nav.add_rudder(rudder)
nav.load_waypoints("waypoints.json")
net.listener()

while nav.running or nav.retHome:
    
    print(nav.depth)

    if not nav.handle_networking(net.recieved):
        nav.running = False
        net.running = False
        sonar.running = False

    try:   time.sleep(0.5)
    except KeyboardInterrupt:
        nav.running = False
        net.running = False
        sonar.running = False

exit()