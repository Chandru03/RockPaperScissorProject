import random

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)  # webcam capture
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0] #[ai,player]

while True:
    imgBg = cv2.imread('Resources/bg.png')  # background image
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.935, 0.935)
    imgScaled = imgScaled[:, 99:500]

    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False: #count till 3 before starting the game
            timer = time.time() - initialTime
            cv2.putText(imgBg, str(int(timer)), (600, 520), cv2.FONT_HERSHEY_PLAIN, 6, (157, 117, 203), 8)

            if timer > 3: #start the game ar the count of 3
                stateResult = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:  # stone
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:  # paper
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:  # scissor
                        playerMove = 3

                    randomNumber = random.randint(1,3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBg = cvzone.overlayPNG(imgBg, imgAI, (150, 360))  # AI hand

                    #player wins
                    if(playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] +=1

                    #ai wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1


    imgBg[320:769, 790:1191] = imgScaled

    if stateResult:
        imgBg = cvzone.overlayPNG(imgBg, imgAI, (150, 360))  # AI hand will stay

    #ai score
    cv2.putText(imgBg, str(scores[0]), (400, 275), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 6)

    #player score
    cv2.putText(imgBg, str(scores[1]), (1120, 275), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 6)
    cv2.imshow("Rock Paper Scissor", imgBg)

    key = cv2.waitKey(1)
    if key == ord(' '): #space to start the game
        startGame = True
        initialTime = time.time()
        stateResult = False
