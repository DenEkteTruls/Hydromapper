import json
import time
import numpy as np
import math


class Nav:

    def __init__(self):

        self.compass = 0
        self.position = {"lat":59.514596190314414,"lng":10.15316963195801}
        self.waypoints = []
        self.running = False


    def report(self, message : str) -> None:

        print(f"[REPORT] {message}")


    def load_waypoints(self, filename : str) -> None:

        with open(filename, "r") as f:
            self.waypoints = json.load(f)
        self.report(f"{len(nav.waypoints)} waypoints loaded!")


    def update_position(self) -> None:

        self.position = {"lat":59.514596190314414,"lng":10.15316963195801}
        # Ikke laget funksjon for dette enda...


    def get_heading(self, pos1 : dict, pos2 : dict) -> int:

        lat1 = pos1["lat"]; long2 = pos1["lng"]
        lat2 = pos2["lat"]; long1 = pos2["lng"]

        dN = lat2-lat1
        dE = long2-long1
        r = 6371*1000
        r2 = r*math.cos(lat1*math.pi/180)
        dNm = math.sqrt(2*(r**2)-2*(r**2)*math.cos(dN*math.pi/180))
        dEm = math.sqrt(2*(r2**2)-2*(r2**2)*math.cos(dE*math.pi/180))

        if dEm == 0: dEm = 0.000000000001
        Vh1 = math.atan(dNm/dEm)*180/math.pi

        if (dN >= 0):
            if (dE >= 0): Vh = 90 - Vh1
            else: Vh = 270+Vh1

        if (dN < 0):
            if (dE >= 0): Vh = 90+Vh1
            else: Vh = 270-Vh1

        return 360-Vh


    def get_distance(self, pos1 : dict, pos2 : dict) -> float:

        r = 6371
        phi1 = np.radians(pos1["lat"])
        phi2 = np.radians(pos2["lat"])
        delta_phi = np.radians(pos2["lat"]-pos1["lat"])
        delta_lambda = np.radians(pos2["lng"]-pos1["lng"])
        a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
        res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

        return res*1000


    def check_if_close(self, pos : dict) -> bool:

        distance = self.get_distance(self.position, pos)
        if distance <= 1:
            return True
        return False

    
    def show_route(self) -> None:

        for pos, waypoint in enumerate(nav.waypoints):
            heading = self.get_heading(self.position, waypoint)
            distance = self.get_distance(self.position, waypoint)
            print(f"[AUTOPILOT] {pos}. Heading: {heading}, Distance: {distance}m")


    def start_autopilot(self) -> None:

        self.running = True
        nav.report("Starting autopilot ..."); time.sleep(2)

        for pos, waypoint in enumerate(nav.waypoints):
            if not self.running: break
            while not self.check_if_close(waypoint):
                if not self.running: break
                self.update_position()

                heading = self.get_heading(self.position, waypoint)
                distance = self.get_distance(self.position, waypoint)
                print(f"[AUTOPILOT] {pos}. Heading: {heading}, Distance: {distance}m")

        nav.report("Route has completed!"); time.sleep(2)
        running = False


nav = Nav()
nav.load_waypoints("waypoints.json")
nav.get_heading(nav.waypoints[0], nav.waypoints[1])

nav.show_route()
#nav.start_autopilot()