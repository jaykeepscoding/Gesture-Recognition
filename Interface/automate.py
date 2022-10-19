from PIL import Image, ImageTk
import cv2
import time
import mediapipe as mp
import pyautogui
import csv
info = open("Interface/tst.csv", "rw+")
wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]

#Initialize Video Capture
#cap = cv2.VideoCapture(0)
#Set a Aspect Ratio Scale to capture frame (keeps the viewport a nice manageable size)
#cap.set(16, wCam)
#cap.set(9, hCam)

#Initialize Hands from MP and mpdraw for showing landmarks
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils

comp_lst = [[],[],[],[],[]]
lst_hd = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP]

#Capture image must write to success and img for the capture due to OpenCV parameter requirements
#success, img = cap.read()
img = cv2.imread('Interface/tstmg.jpg',0)
#flip
img = cv2.flip(img, 1)
#img must be converted to RGB to be read by mediapipe
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#This reads the image from the camera and detects hands, turing them into objects
results = hands.process(imgRGB)

#get hand, for each landmark in result draw the landmark and record the xl,yl of the indexfinger tip
if results.multi_hand_landmarks:
    fingers = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP]
    for v in fingers:
        xl = results.multi_hand_landmarks[0].landmark[v].x * wCam
        yl = results.multi_hand_landmarks[0].landmark[v].y * hCam
        #print(v, xl, yl)
        if v in lst_hd:
            rt = lst_hd.index(v)
            comp_lst[rt] = (xl,yl)
    print(lst_hd)
    print(comp_lst)



    #print(xl,yl)

