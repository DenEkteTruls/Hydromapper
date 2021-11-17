from nav import Nav
from esc import ESC
from rudder import Rudder
from networking import Networking
import pigpio
import time

pi = pigpio.pi()
nav = Nav()
esc = ESC(esc_pin = 4, pi = pi)
rudder = Rudder(pin = 17, pi = pi)
net = Networking("localhost", 8081, 1024)

nav.add_esc(esc)
nav.add_rudder(rudder)
nav.load_waypoints("waypoints.json")
net.listener()

while nav.running or nav.retHome:

    if not nav.handle_networking(net.recieved):
        nav.running = False
        net.running = False
    time.sleep(0.5)

exit()