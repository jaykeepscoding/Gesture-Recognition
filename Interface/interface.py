import tkinter
from tkinter import *
from PIL import Image, ImageTk
import cv2
import time
import pyautogui
import mediapipe as mp
import keyboard
import pyautogui
class Interface():
   def __init__(self):
      self.win = Tk()
      #Operations(self.win)
      optics_inst = opticsControl(self.win)

      tkinter.Button(self.win, text="Kill feed", command=optics_inst.setCamera).pack()
      self.win.mainloop()


class Operations():
   def __init__(self, win):
      self.win = win

      tkinter.Button(self.win, text="Calibrate", command=Operations.calibrate).pack()
   def calibrate():
      #tkinter.Button(self.win, text="Calibrate").pack()
      print("A")


   def killFeed(self):
      return 0
   def exit(self):
      return 0
   def reset(self):
      return 0

class opticsControl():
   def __init__(self, win):
      self.win = win
      self.cameraOn = 1
      self.labeler = Label(self.win, width=150, height=100, bg='black')

      self.cap = cv2.VideoCapture(0)
      self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
      self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)


      self.startFeed()
      self.labeler.pack()


   def startFeed(self):
      wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]
      mpHands = mp.solutions.hands
      hands = mpHands.Hands()
      mpdraw = mp.solutions.drawing_utils

      _, frame = self.cap.read()
      cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

      img = Image.fromarray(cv2image)
      #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      results = hands.process(cv2image)

      if results.multi_hand_landmarks:
         if keyboard.is_pressed('Ctrl'):
            exit()

         xl = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * wCam
         yl = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * hCam
         print(xl, yl)
         pyautogui.moveTo(xl, yl)
      # Convert image to PhotoImage
      imgtk = ImageTk.PhotoImage(image=img)
      self.labeler.imgtk = imgtk
      self.labeler.configure(image=imgtk)
      # Repeat after an interval to capture continiously
      self.labeler.after(20, self.startFeed)

   def setCamera(self):
      pass
   def getCamera(self):
      pass
   def readFeed(self):
      return 0

instance = Interface()

