import os
import json
import time
import numpy as np
import threading
import geopy.distance

#
#   0x1000 > 0x1100     : Speed
#   0x0001              : Arm
#   0x0010              : Disarm
#   1x0000              : Return to Home (first waypoint)
#   1x0001              : Start Autopilot
#   1x0011              : Stop Autopilot
#   2x-60 > 2x+60       : Rudder heading (direct)
#

class Nav:

    def __init__(self):

        self.GPS = ""
        self.escs = []
        self.rudders = []
        self.GPScompass = 0
        self.position = {}
        self.waypoints = []
        self.retHome = False
        self.running = True
        self.autopilot_running = True
        self.depth = None
        self.offset = 0


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

            if msg[0:3] == "0x1":
                for esc in self.escs:
                    print(msg[3:])
                    esc.set(int(msg[3:]))

            elif msg[0:2] == "2x":
                try:
                    self.heading = int(msg[2:5])
                    print(self.heading)
                except:
                    break

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

            elif msg == "1x0011":
                self.stop_autopilot()

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
                #x, y = utm.from_latlon(wp["lat"], wp["lng"])[0:2]
                x = wp['lat']
                y = wp['lng']
                self.waypoints.append({'x': x, 'y': y})

        self.report(f"{len(self.waypoints)} waypoints loaded!")


    def get_heading(self, pos1 : dict, pos2 : dict) -> int:


        lat1 = np.radians(pos1['x'])
        lat2 = np.radians(pos2['x'])

        diffLong = np.radians(pos2['y'] - pos1['y'])
        
        x = np.sin(diffLong) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) * np.cos(diffLong))

        initial_bearing = np.rad2deg(np.arctan2(x, y))
        compass_bearing = (initial_bearing + 360) % 360

        return int(compass_bearing)


    def get_distance(self, pos1 : dict, pos2 : dict) -> float:

       #R = 6373.0

       #lat1 = np.radians(pos1['x'])
       #lat2 = np.radians(pos2['x'])
       #lon1 = np.radians(pos1['y'])
       #lon2 = np.radians(pos2['y'])

       #dlon = lon2 - lon1
       #dlat = lat2 - lat1

       #a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
       #c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

       #distance = int(R * c * 1000)

       #return distance

       cords1 = (pos1['x'], pos1['y'])
       cords2 = (pos2['x'], pos2['y'])

       return geopy.distance.distance(cords1, cords2).m


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

            heading = self.get_heading(self.position, self.waypoints[0])
            distance = self.get_distance(self.position, self.waypoints[0])
            if print_: print(f"[AUTOPILOT] ** RETURNING HOME **  Distance: {distance}"); print_ = False

    
    def return_home(self) -> None:

        threading._start_new_thread(self.return_home_, ())



    def start_autopilot_(self) -> None:

        self.report("Starting autopilot ..."); time.sleep(1.5)
        
        last_time = time.time()
        print_ = False

        for i, waypoint in enumerate(self.waypoints):
            while not self.check_if_close(waypoint):
                
                if not self.running or not self.autopilot_running or self.retHome: break

                if time.time() - last_time > 1:
                    print_ = True; last_time = time.time()

                heading = self.get_heading(self.position, waypoint)
                distance = self.get_distance(self.position, waypoint)

                self.offset = heading - self.GPScompass
                
                #for rudder in self.rudders:
                #    rudder.heading_compansation(offset)

                if print_: print(f"[AUTOPILOT] {i}\tHeading: {heading}\tGPScompass: {self.GPScompass}\tDistance: {distance}m\tPosition: {self.position}\t{waypoint}"); print_ = False

            # code for quick turn to waypoint

        self.report("Route has completed!"); time.sleep(1.5)
        self.running = False


    def start_autopilot(self) -> None:

        threading._start_new_thread(self.start_autopilot_, ())


    def stop_autopilot(self) -> None:
        
        self.autopilot_running = False


#nav = Nav()
#nav.load_waypoints("waypoints.json")
#nav.get_heading(nav.waypoints[0], nav.waypoints[1])

#nav.show_simulated_route()
#nav.start_autopilot()
