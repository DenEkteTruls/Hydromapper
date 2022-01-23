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
        position = json.loads(line[line.index("{"):line.index("}")+1])

        point = {
            "pos": i,
            "lat": position['lat'],
            "lng": position['lng']
        }

        image = cv2.imread(f"samples/{point['pos']}.jpg")
        cv2.imshow("frame", image)
        cv2.waitKey(10)

        point['depth'] = float(input(f"Depth: "))
        points.append(point)


print(points)

"""

try:
        with open("checked_data.json", "r") as f:
	    points = json.loads(f.read())
except:
    pass

with open("checked_data.json", "w") as f:

    for p in points:
        p['lat']
        p['lng']

    f.write(json.dumps(points))