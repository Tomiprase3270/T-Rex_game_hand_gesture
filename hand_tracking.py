import cv2
import mediapipe as mp
import time


cam = cv2.VideoCapture(0)

#Class Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


currentTime = 0
prevoiusTime = 0
while True:
    success, webcam = cam.read()
    imgRGB = cv2.cvtColor(webcam, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    #Hand landmark draws
    if results.multi_hand_landmarks:
        for MultiHandLandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(MultiHandLandmarks.landmark):
                #print(id,lm)

               #untuk mengecek koordinat titik pada landamrak tangan pada webcam
                h, w, c = webcam.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:
                    cv2.circle(webcam, (cx, cy), 17, (255, 0, 255), cv2.FILLED)


            mpDraw.draw_landmarks(webcam, MultiHandLandmarks, mpHands.HAND_CONNECTIONS)

    currentTime = time.time()
    fps = 1 / (currentTime - prevoiusTime)
    prevoiusTime = currentTime

    cv2.putText(webcam, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


    cv2.imshow("camera", webcam)
    cv2.waitKey(1)