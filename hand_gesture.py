import cv2
import numpy as np
import time
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

#setting wide and high camera
wCam, hCam = 640, 488

#variable of web camera
cam = cv2.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)

#variable for FPS
previousTime = 0

detector = htm.HandDetector()

#volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volBar = 400





while True:
    success, webcam = cam.read()
    webcam = detector.findHands(webcam)
    lmList = detector.findHandPosition(webcam, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(webcam, (x1, y1), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(webcam, (x2, y2), 12, (255, 0, 255), cv2.FILLED)
        cv2.line(webcam, (x1,y1), (x2,y2), (255,0,255), 3)
        cv2.circle(webcam, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #print(length)

        # hand range = 10 - 150
        # vol range = -65 - 0

        vol = np.interp(length, [10,150], [minVol, maxVol])
        volBar = np.interp(length, [10, 150], [400, 85])
        #print(int(length), vol)
        # volume.SetMasterVolumeLevel(vol, None)
        if length<12:
            cv2.circle(webcam, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        #press space
        if length > 80:
            pyautogui.press("space")



    cv2.rectangle(webcam, (50,150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(webcam, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)





    # Frame Per Second
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv2.putText(webcam, f'FPS : {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)


    cv2.imshow("webcam", webcam)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()