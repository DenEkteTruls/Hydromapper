import cv2
import numpy as np
from numpy.core.defchararray import upper
import pytesseract as pt

cap = cv2.VideoCapture(0)
pt.pytesseract.tesseract_cmd = "C:/Program files/Tesseract-OCR/tesseract.exe"

while True:

    frame = cap.read()[1]

    HSV = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), (480, 360))

    sensitivity = 50
    lower_white = np.array([0, 0, 255-sensitivity])
    upper_white = np.array([255, sensitivity, 255])

    mask = cv2.inRange(HSV, lower_white, upper_white)
    HSV = cv2.bitwise_and(HSV, HSV, mask = mask)

    d = pt.image_to_data(HSV, config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.", output_type = pt.Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(HSV, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    print(d['text'])

    cv2.imshow("frame", frame)
    cv2.imshow("masked", HSV)

    if cv2.waitKey(10) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()
