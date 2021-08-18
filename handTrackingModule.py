import cv2
import mediapipe as mp
import time


#Class Hands
class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackingCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, webcam, draw=True):
        imgRGB = cv2.cvtColor(webcam, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #Hand landmark draws
        if self.results.multi_hand_landmarks:
            for MultiHandLandmarks in self.results.multi_hand_landmarks:
                for id, lm in enumerate(MultiHandLandmarks.landmark):
                    if draw:
                        self.mpDraw.draw_landmarks(webcam, MultiHandLandmarks, self.mpHands.HAND_CONNECTIONS)
        return webcam

    # untuk mengecek koordinat titik pada landamrak tangan pada webcam
    def findHandPosition(self, webcam, handNumber=0, draw=True):

        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = webcam.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(webcam, (cx, cy), 12, (255, 0, 255), cv2.FILLED)

        return lmList


def main():

    #Variable

    currentTime = 0
    prevoiusTime = 0
    cam = cv2.VideoCapture(0)

    #nyoba dalam 1 file
    detector = HandDetector()

    while True:
        success, webcam = cam.read()
        webcam = detector.findHands(webcam)
        lmList = detector.findHandPosition(webcam)
        if len(lmList) != 0:
            print(lmList[4])

        #Frame Per Second
        currentTime = time.time()
        fps = 1 / (currentTime - prevoiusTime)
        prevoiusTime = currentTime
        cv2.putText(webcam, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        #show the webcam
        cv2.imshow("camera", webcam)
        cv2.waitKey(1)




if __name__ == "__main__":
    main()