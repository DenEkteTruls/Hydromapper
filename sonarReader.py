import cv2
import numpy as np
import pytesseract as pt

cap = cv2.VideoCapture(0)
depthBuffer = []
depth = None

while True:

    frame = cap.read()[1]

    gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (480, 360))

    """sensitivity = 60
    lower_white = np.array([0, 0, 255-sensitivity])
    upper_white = np.array([255, sensitivity, 255])"""

    """mask = cv2.inRange(HSV, lower_white, upper_white)
    HSV = cv2.bitwise_and(HSV, HSV, mask = mask)
    HSV = cv2.GaussianBlur(HSV, (3, 3), 0)"""


    d = pt.image_to_data(gray, config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.", output_type = pt.Output.DICT)

    # filter
    try    : depthBuffer.append(float(d['text'][4]))
    except : pass

    if len(depthBuffer) > 1:
        depth = max(set(depthBuffer), key = depthBuffer.count)
        depthBuffer = []

    print(depth)

    cv2.imshow("frame", gray)
    #cv2.imshow("masked", HSV)

    if cv2.waitKey(10) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()
