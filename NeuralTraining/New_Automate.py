from PIL import Image, ImageTk
import cv2
import time
import mediapipe as mp
import pyautogui
import csv
import glob, os
import numpy as np
#info = open("Interface/tst.csv", "rw+")
def populate_folder(image_counter):

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
    type_of_picture = int(input("Hand Sign Number? "))
    while(True):
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        cv2.imshow('frame', frame)
        cv2.setWindowProperty('frame',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)
        if cv2.waitKey(1) == ord('q'):
            break
        if cv2.waitKey(1) == ord('w'):
           cv2.imwrite("training_data/".format(type_of_picture)+"{}-{}.jpg".format(type_of_picture,image_counter), frame)
           image_counter += 1
    cap.release()
    finished = int(input("Finished? (1 for yes, 0 for no) "))
    if finished == 0:
        populate_folder(image_counter)
    return image_counter
def createList(aimage):
    #wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpdraw = mp.solutions.drawing_utils

    
    img = cv2.imread(aimage,0)

    #img = cv2.flip(img, 1)
    comp = []
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    with mpHands.Hands(min_detection_confidence=0.001, min_tracking_confidence=.01) as hands:
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            fingers = [mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP,mpHands.HandLandmark.WRIST]
            for v in fingers:
                xl = results.multi_hand_landmarks[0].landmark[v].x
                yl = results.multi_hand_landmarks[0].landmark[v].y
                #print(v, xl, yl)
                if v in fingers:
                    comp.append(xl)
                    comp.append(yl)
    return comp

#populate_folder(0)
images = []
classifiers = []
#folder = input("enter folder name: ")
folder = "training_data"
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith(".jpg"):
            images.append(os.path.join(root,file))
            classifiers.append(file[0])

folderRes = 'training_data' + '/' + folder + '.csv'
count = -1
with open(folderRes, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    #spamwriter.writerow("THUMB INDEX MIDDLE RING PINKY")
    
    for x in images:
            count += 1
            tst = createList(x)
            print(classifiers[count])
            tst.insert(0, int(classifiers[count]))
            if len(tst) > 1:
                        #csv_writer.writerow((str(tst[0][y])[13:][:-4]))
                #csv_writer.writerow(tst)
                csv_writer.writerow(tst)
            else:
                pass
