from PIL import Image, ImageTk
import cv2
import time
import mediapipe as mp
import pyautogui
import csv
import glob, os

#info = open("Interface/tst.csv", "rw+")
def createList(aimage):
    wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpdraw = mp.solutions.drawing_utils

    comp_lst = [[],[],[],[],[]]
    lst_hd = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP]
    newp = {}

    img = cv2.imread(aimage,0)

    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        fingers = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP]
        for v in fingers:
            xl = results.multi_hand_landmarks[0].landmark[v].x * wCam
            yl = results.multi_hand_landmarks[0].landmark[v].y * hCam
            #print(v, xl, yl)
            if v in lst_hd:

                newp[str(v)] = (xl,yl)

    print(newp)

    return newp
images = []
for root, dirs, files in os.walk("images"):
    for file in files:
        if file.endswith(".jpg"):
            images.append(os.path.join(root,file))
print(images)
with open('imagedata.csv', 'w', newline='') as csvfile:
    fieldnames = ['HandLandmark.RING_FINGER_TIP','HandLandmark.THUMB_TIP','HandLandmark.PINKY_TIP','HandLandmark.INDEX_FINGER_TIP','HandLandmark.MIDDLE_FINGER_TIP']

    csv_writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
    #spamwriter.writerow("THUMB INDEX MIDDLE RING PINKY")
    for x in images:
            print(x)
            tst = createList(x)
            print(type(tst), len(tst))
            if len(tst) != 0:
                csv_writer.writeheader()


                        #csv_writer.writerow((str(tst[0][y])[13:][:-4]))
                csv_writer.writerow(tst)
            else:
                pass
