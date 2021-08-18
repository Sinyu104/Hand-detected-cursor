import cv2, time
from threading import Thread, Lock
import HandTrackingModule as htm
import numpy as np
from pynput.mouse import Button, Controller
from datetime import datetime

##########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
wScr = 1280
hScr = 720
#########################

class VideoCap:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)
        self.pTime = 0
        self.fps = 0
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        self.detector = htm.handDetector(maxHands=1)
        self.mouse = Controller()
        self.stopped = False
        self.lock = Lock()
        (self.success, self.img) = self.cap.read()
        
    def start(self):    
        self.thd1=Thread(target=self.get, args=())
        self.thd1.daemon=True
        self.thd1.start()
        
    
    def get(self):
        while not self.stopped:
            print("In get Thread")
            success, img = self.cap.read()
            self.lock.acquire()
            (self.success, self.img) = success, img
            self.lock.release()
            
            

    def detect(self):
        print("In detect Thread")
        self.lock.acquire()
        img = self.img.copy()
        self.lock.release()
        img = self.detector.findHands(img)
        self.lmList, self.bbox = self.detector.findPosition(img)
        if len(self.lmList) != 0:
            x1, y1 = self.lmList[8][1:]
            x2, y2 = self.lmList[12][1:]
            # print(x1, y1, x2, y2)
        
            # 3. Check which fingers are up
            fingers = self.detector.fingersUp()
            # print(fingers)
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
            # 4. Only Index Finger : Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                # 6. Smoothen Values
                self.clocX = self.plocX + (x3 - self.plocX) / smoothening
                self.clocY = self.plocY + (y3 - self.plocY) / smoothening
                print(wScr-x3,y3)
                # 7. Move Mouse
                
                self.mouse.position = (wScr - self.clocX, self.clocY)
                print('Now we have moved it to {0}'.format(self.mouse.position))
                #autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                self.plocX, self.plocY = self.clocX, self.clocY
            
            # 8. Both Index and middle fingers are up : Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                # 9. Find distance between fingers
                length, img, lineInfo = self.detector.findDistance(8, 12, img)
                print(length)
                # 10. Click mouse if distance short
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    self.mouse.press(Button.left)
                    self.mouse.release(Button.left)
        
        self.cTime = time.time()
        self.fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        cv2.putText(img, str(self.fps), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
        cv2.imshow("Video", img)
        
        
    
    # def show(self):
    #     print("In show function")
    #     self.lock.acquire()
    #     img = self.img.copy()
    #     self.lock.release()
    #     cv2.putText(img, str(self.fps), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    #     cv2.imshow("Video", img)

    
vc = VideoCap(0)
vc.start()
while True:
    vc.detect()
    if cv2.waitKey(50) == ord("q"):
        break
    