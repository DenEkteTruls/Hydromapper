import os
import utm
import json
import time
import numpy as np
import threading


#
#   0x1000 > 0x1100     : Speed
#   0x0001              : Arm
#   0x0010              : Disarm
#   1x0000              : Return to Home (first waypoint)
#   1x0001              : Start Autopilot
#   2x-60 > 2x+60       : Rudder heading (direct)
#

class Nav:

    def __init__(self):

        self.escs = []
        self.rudders = []
        self.compass = 0
        self.position = {}
        self.waypoints = []
        self.retHome = False
        self.running = True

        os.system("sudo pigpiod")


    def report(self, message : str) -> None:

        print(f"[NAV] {message}")

    
    # def add_esc(self, esc : object | list) -> None: (python3.10)
    def add_esc(self, esc : object) -> None:

        if isinstance(esc, object):
            self.escs.append(esc)
            self.report("Added ESC")

        elif isinstance(esc, list):
            for esc_ in esc:
                self.escs.append(esc_)
            self.report(f"Added {len(esc)} ESCs")

    #def add_rudder(self, rudder : object | list) -> None: (python3.10)
    def add_rudder(self, rudder : object) -> None:

        if isinstance(rudder, object):
            self.rudders.append(rudder)
            self.report("Added rudder")

        elif isinstance(rudder, list):
            for rudder_ in rudder:
                self.rudders.append(rudder_)
            self.report(f"Added {len(rudder)} rudders")


    def handle_networking(self, recieved : list) -> bool:

        for msg in recieved:

            if msg[0:2] == "0x1":
                for esc in self.escs:
                    esc.set(msg[3:])

            elif msg[0:2] == "2x":
                try:
                    self.heading = int(msg[3:5])
                except:
                    break

                print(f"New heading : {self.heading}")
                for rudder in self.rudders:
                    rudder.set_heading(int(self.heading))

            elif msg == "0x0001":
                for esc in self.escs:
                    esc.arm()

            elif msg == "0x0010":
                for esc in self.escs:
                    esc.disarm()

            elif msg == "1x0000":
                self.return_home()

            elif msg == "1x0001":
                self.start_autopilot()

            elif msg == "stop" or msg == "quit":
                self.retHome = False
                for esc in self.escs:
                    esc.disarm()
                return False


            # (python3.10)
            """
            match msg:

                case "0x0001":
                    for esc in self.escs:
                        esc.arm()

                case "0x0010":
                    for esc in self.escs:
                        esc.disarm()

                case "1x0000":
                    self.return_home()

                case "1x0001":
                    self.start_autopilot()

                case "stop" | "quit":
                    self.retHome = False
                    for esc in self.escs:
                        esc.disarm()
                    return False
            """
            
            recieved.remove(msg)

        return True



    def load_waypoints(self, filename : str) -> None:

        with open(filename, "r") as f:
            waypoints = json.load(f)
            for wp in waypoints:
                x, y = utm.from_latlon(wp["lat"], wp["lng"])[0:2]
                self.waypoints.append({'x': x, 'y': y})

        self.report(f"{len(self.waypoints)} waypoints loaded!")


    def update_position(self) -> None:

        x, y = utm.from_latlon(59.51641635461993, 10.1494038105011)[0:2]
        self.position = {'y': y, 'x': x}
        # Ikke laget funksjon for dette enda...


    def get_heading(self, pos1 : dict, pos2 : dict) -> int:

        dN = abs(pos1['y']-pos2['y'])
        dE = abs(pos1['x']-pos2['x'])

        return np.rad2deg(np.arctan(dN/dE)) - 1


    def get_distance(self, pos1 : dict, pos2 : dict) -> float:

        dN = abs(pos1['y']-pos2['y'])
        dE = abs(pos1['x']-pos2['x'])

        return np.sqrt(dN**2 + dE**2)


    def check_if_close(self, pos : dict) -> bool:

        if self.position:
            distance = self.get_distance(self.position, pos)
            if distance <= 2: # 2m^2
                return True
        return False


    def show_simulated_route(self) -> None:

        for pos, wp in enumerate(self.waypoints[:-1]):
            heading = self.get_heading(wp, self.waypoints[pos+1])
            distance = self.get_distance(wp, self.waypoints[pos+1])
            print(f"[AUTOPILOT SIMULATION] {pos}. Heading: {heading}, Distance: {distance}m")


    def return_home_(self) -> None:

        self.retHome = True
        last_time = time.time()
        print_ = False

        while not self.check_if_close(self.waypoints[0]):
            if not self.retHome: break
            if time.time() - last_time > 1:
                print_ = True; last_time = time.time()

            self.update_position()
            heading = self.get_heading(self.position, self.waypoints[0])
            distance = self.get_distance(self.position, self.waypoints[0])
            if print_: print(f"[AUTOPILOT] ** RETURNING HOME **  Distance: {distance}"); print_ = False

    
    def return_home(self) -> None:

        threading._start_new_thread(self.return_home_, ())


    def start_autopilot_(self) -> None:

        self.report("Starting autopilot ..."); time.sleep(1.5)
        
        last_time = time.time()
        print_ = False

        for pos, waypoint in enumerate(self.waypoints):
            while not self.check_if_close(waypoint):

                if not self.running or self.retHome: break

                if time.time() - last_time > 1:
                    print_ = True; last_time = time.time()
                
                self.update_position()
                heading = self.get_heading(self.position, waypoint)
                distance = self.get_distance(self.position, waypoint)
                if print_: print(f"[AUTOPILOT] {pos}. Heading: {heading}, Distance: {distance}m"); print_ = False


        self.report("Route has completed!"); time.sleep(1.5)
        self.running = False


    def start_autopilot(self) -> None:

        threading._start_new_thread(self.start_autopilot_, ())


#nav = Nav()
#nav.load_waypoints("waypoints.json")
#nav.get_heading(nav.waypoints[0], nav.waypoints[1])

#nav.show_simulated_route()
#nav.start_autopilot()