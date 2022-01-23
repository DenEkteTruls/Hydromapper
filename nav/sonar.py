import cv2
import pytesseract as pt
import threading


class Sonar:
    
    def __init__(self, nav : object) -> None:
        
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.depth = None
        self.nav = nav

    
    def run_(self) -> None:

        while self.running:

            frame = self.cap.read()[1]
            gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (480, 360))
            d = pt.image_to_data(gray, config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.", output_type = pt.Output.DICT)

            try     : self.depth = float(d['text'][4])
            except  : pass

            self.nav.depth = self.depth
            self.nav.depthshot = gray

            self.nav.save_data(self.nav.position, self.depth, self.nav.heading, gray)
            
        self.cap.release()
        self.running = False


    def run_in_background(self):

        threading._start_new_thread(self.run_, ())
