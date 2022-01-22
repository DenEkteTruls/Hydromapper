import os
import cv2
import json
import time
from turtle import position
import numpy as np
import threading
from geographiclib.geodesic import Geodesic

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

        self.GPS = []
        self.escs = []
        self.rudders = []
        self.position = {}
        self.waypoints = []
        self.retHome = False
        self.running = True
        self.autopilot_running = True
        self.depth = -1
        self.depthshot = None
        self.offset = 0
        self.sample_ticker = 0
        self.heading = -1
        self.sats = -1


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
                x = wp['lat']
                y = wp['lng']
                self.waypoints.append({'lat': x, 'lng': y})

        self.report(f"{len(self.waypoints)} waypoints loaded!")


    def get_heading(self, pos1 : dict, pos2 : dict) -> int:

        if (len(pos1) > 0 and len(pos2) > 0) or not pos1['lat'] == None or not pos2['lat'] == None:

            a = Geodesic.WGS84.Inverse(pos1['lat'], pos1['lng'], pos2['lat'], pos2['lng'])

            bearing = a['azi1']
            if bearing < 0:
                bearing += 360
            return round(bearing, 2)
        else:
            return False


    def get_distance(self, pos1 : dict, pos2 : dict) -> float:

        if (len(pos1) > 0 and len(pos2) > 0) or not pos1['lat'] == None or not pos2['lat'] == None:
            a = Geodesic.WGS84.Inverse(pos1['lat'], pos1['lng'], pos2['lat'], pos2['lng'])
            return round(a['s12'], 2)
        else:
            return False


    def check_if_close(self, pos : dict) -> bool:

        if self.position:
            distance = self.get_distance(self.position, pos)
            if distance <= 2: # 2m^2
                return True
        return 
        
    
    def save_data(self, position, depth, heading, image):

        if not depth == -1 and image.any():
            with open("saved_data.json", "a") as f:
                f.write(f"{self.sample_ticker},{position},{depth},{heading}")
            cv2.imwrite(f"samples/{self.sample_ticker}.jpg", image)
            print(f"[SAVE DATA]\t{self.sample_ticker},{position},{depth},{heading}")
            self.sample_ticker += 1


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

                self.offset = int(heading - self.heading)
                print(f"Heading to WP: {heading}\tHeading: {round(self.heading, 2)}\tOffset: {self.offset}\tDistance: {distance}")

                #for esc in self.escs:
                #    esc.distance_compansation(distance)

                for rudder in self.rudders:
                    rudder.heading_compansation(self.offset)

                if print_:
                    pass
                    #self.save_data(self.position, self.depth, self.heading, self.depthshot)
                    #print(f"[AUTOPILOT] {i}\tSatellites: {self.sats}\tHeading: {self.heading}\tOffset: {self.offset}\tDistance: {distance}m\tPosition: {self.position}"); print_ = False

            # code for quick turn to waypoint (or not)

        self.report("Route has completed!"); time.sleep(1.5)
        self.running = False

        self.return_home()


    def start_autopilot(self) -> None:

        threading._start_new_thread(self.start_autopilot_, ())


    def stop_autopilot(self) -> None:
        
        self.autopilot_running = False


#nav = Nav()
#nav.load_waypoints("waypoints.json")
#nav.get_heading(nav.waypoints[0], nav.waypoints[1])

#nav.show_simulated_route()
#nav.start_autopilot()
