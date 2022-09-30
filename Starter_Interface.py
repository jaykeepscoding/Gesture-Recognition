import pyautogui
import cv2
import mediapipe as mp
import time
import keyboard
#Width and Height of Monitor
wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]

#Initialize Video Capture
cap = cv2.VideoCapture(0)

#Set a Aspect Ratio Scale to capture frame (keeps the viewport a nice manageable size)
cap.set(16, wCam)
cap.set(9, hCam)

#Initialize Hands from MP and mpdraw for showing landmarks
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils

while True:
    #Capture image must write to success and img for the capture due to OpenCV parameter requirements
    success, img = cap.read()
    #flip
    img = cv2.flip(img, 1)
    #img must be converted to RGB to be read by mediapipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #This reads the image from the camera and detects hands, turing them into objects
    results = hands.process(imgRGB)

    #get hand, for each landmark in result draw the landmark and record the xl,yl of the indexfinger tip
    if results.multi_hand_landmarks:
        if keyboard.is_pressed('Ctrl'):
            exit()

        xl = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * wCam
        yl = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * hCam
        print(xl,yl)
        pyautogui.moveTo(xl,yl)





    
