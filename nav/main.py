from nav import Nav
from esc import ESC
from networking import Networking
import time

nav = Nav()
esc = ESC(esc_pin = 4)
net = Networking("localhost", 8081, 1024)

nav.add_esc(esc)
nav.load_waypoints("waypoints.json")
net.listener()

while nav.running:

    if not nav.handle_networking(net.recieved):
        nav.running = False
        net.running = False
    time.sleep(0.5)

exit()