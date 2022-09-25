import pyautogui
import cv2
import mediapipe as mp
import time
wCam, hCam = 1920,1080

cap = cv2.VideoCapture(0)

cap.set(16, wCam)
cap.set(9, hCam)


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils
ptime = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(img, handlms)
            xl = handlms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * wCam
            yl = handlms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * hCam
            
            pyautogui.moveTo(xl,yl)
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img, f"FPS: {int(fps)}", (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
    cv2.imshow("Img", img)
    cv2.waitKey(1)
    
    
