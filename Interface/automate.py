from PIL import Image, ImageTk
import cv2
import time
import mediapipe as mp
import pyautogui
import csv
import glob, os

#info = open("Interface/tst.csv", "rw+")
def createList(aimage):
    #wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpdraw = mp.solutions.drawing_utils

    comp_lst = [[],[],[],[],[]]
    lst_hd = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP,mpHands.HandLandmark.WRIST]
    newp = {}
    img = cv2.imread(aimage,0)
    #cv2.imshow("", img)
    #cv2.waitKey(0)

    #img = cv2.flip(img, 1)
    wCam = img.shape[0]
    hCam = img.shape[1]
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    with mpHands.Hands(min_detection_confidence=0.001, min_tracking_confidence=.01) as hands:
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            fingers = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP,mpHands.HandLandmark.WRIST]
            for v in fingers:
                xl = results.multi_hand_landmarks[0].landmark[v].x * wCam
                yl = results.multi_hand_landmarks[0].landmark[v].y * hCam
                #print(v, xl, yl)
                if v in lst_hd:
                    newp[str(v)] = (xl,yl)

    return newp

def createNormList(aimage):
    #wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpdraw = mp.solutions.drawing_utils
    lst_hd = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP,mpHands.HandLandmark.WRIST]
    newp = {}

    img = cv2.imread(aimage,0)

    #img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    with mpHands.Hands(min_detection_confidence=0.001, min_tracking_confidence=.01) as hands:
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            fingers = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP, mpHands.HandLandmark.WRIST]
            for v in fingers:
                xl = results.multi_hand_landmarks[0].landmark[v].x
                yl = results.multi_hand_landmarks[0].landmark[v].y
                zl = results.multi_hand_landmarks[0].landmark[v].z
                #print(v, xl, yl)
                if v in lst_hd:
                    newp[str(v)] = (xl,yl,zl)
    return newp
images = []
folder = input("enter folder name: ")
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith(".jpg"):
            images.append(os.path.join(root,file))
folderRes = folder + '/' + folder + 'ImageData.csv'
with open(folderRes, 'w', newline='') as csvfile:
    fieldnames = ['HandLandmark.RING_FINGER_TIP','HandLandmark.THUMB_TIP','HandLandmark.PINKY_TIP','HandLandmark.INDEX_FINGER_TIP','HandLandmark.MIDDLE_FINGER_TIP','HandLandmark.WRIST']

    csv_writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
    #spamwriter.writerow("THUMB INDEX MIDDLE RING PINKY")
    for x in images:
            tst = createList(x)
            tst2 = createNormList(x)
            if len(tst) != 0:
                csv_writer.writeheader()


                        #csv_writer.writerow((str(tst[0][y])[13:][:-4]))
                csv_writer.writerow(tst)
                csv_writer.writerow(tst2)
            else:
                pass
