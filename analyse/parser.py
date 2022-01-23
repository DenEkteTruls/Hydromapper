import cv2
import time
import json

points = []

"""

with open("saved_data.json", "r") as f:
    data = f.readlines()
    for line in data:

        splt = line.split(",")

        i = int(splt[0])
        depth = round(float(splt[3]), 2)
        speed = float(splt[4])/100
        position = json.loads(line[line.index("{"):line.index("}")+1])

        point = {
            "pos": i,
            "depth": depth,
            "speed": speed,
            "lat": position['lat'] + -0.0010921,
            "lng": position['lng'] + 0.0081944
        }

        image = cv2.imread(f"samples/{point['pos']}.jpg")
        cv2.imshow("frame", image)
        cv2.waitKey(10)

        point['depth'] = float(input(f"Depth: "))
        points.append(point)


print(points)

"""

with open("checked_data.json", "r") as f:
    points = json.loads(f.read())

with open("checked_data.json", "w") as f:

    for p in points:
        p['lat'] += -0.0010921
        p['lng'] += 0.0081944

    f.write(json.dumps(points))