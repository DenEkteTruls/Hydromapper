import cv2
import json

with open("saved_data.json", 'r') as f:
    lines = f.readlines()
    for line in lines:
        splt = line.split(",")
        i = int(splt[0])
        position = json.loads(line[line.index("{"):line.index("}")+1])

        image = cv2.imread(f"new_samples/{i}.jpg")
        cv2.imshow("image", image)
        cv2.waitKey(10)
        depth = float(input("NEW: "))

        with open("checked_data.json", "a") as f:
            f.write(f"{i},{position['lat']},{position['lng']},{depth}\n")