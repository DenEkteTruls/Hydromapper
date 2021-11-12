import utm
import json
import time
import numpy as np
import math


class Nav:

    def __init__(self):

        self.escs = []
        self.compass = 0
        self.position = {}
        self.waypoints = []
        self.running = False


    def report(self, message : str) -> None:

        print(f"[NAV] {message}")

    
    def add_esc(self, esc : object | list) -> None:

        if isinstance(esc, object):
            self.escs.append(esc)
            self.report("Added ESC")

        elif isinstance(esc, list):
            for esc_ in esc:
                self.escs.append(esc_)
            self.report(f"Added {len(esc)} ESCs")
            

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


    def start_autopilot(self) -> None:

        self.running = True
        self.report("Starting autopilot ..."); time.sleep(2)

        for pos, waypoint in enumerate(self.waypoints):
            if not self.running: break
            while not self.check_if_close(waypoint):
                if not self.running: break
                self.update_position()

                heading = self.get_heading(self.position, waypoint)
                distance = self.get_distance(self.position, waypoint)
                print(f"[AUTOPILOT] {pos}. Heading: {heading}, Distance: {distance}m")

        self.report("Route has completed!"); time.sleep(2)
        self.running = False


#nav = Nav()
#nav.load_waypoints("waypoints.json")
#nav.get_heading(nav.waypoints[0], nav.waypoints[1])

#nav.show_simulated_route()
#nav.start_autopilot()