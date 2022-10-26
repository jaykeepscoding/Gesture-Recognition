import tkinter
from tkinter import *
from PIL import Image, ImageTk
import cv2
import time
import pyautogui
import mediapipe as mp
import keyboard
import pyautogui
import tkinter.ttk as ttk
from tkinter.ttk import *
from ttkthemes import ThemedTk
from memory_profiler import profile
class Interface():
   def __init__(self):
      self.win = Tk()
      s = ttk.Style()

      s.theme_use('xpnative')
      self.win.title("Gesture Interface")
      self.win.wm_attributes('-toolwindow', 'True')
      self.win.wm_attributes('-topmost', 'True')
      self.win.resizable(0,0)
      opticsControl(self.win)
      self.win.mainloop()


class Operations():
   def __init__(self, win):
      self.win = win

      tkinter.Button(self.win, text="Calibrate", command=Operations.calibrate).pack()
   def calibrate():
      #tkinter.Button(self.win, text="Calibrate").pack()
      print("A")

class opticsControl():
   @profile
   def __init__(self, win):
      self.mpHands = mp.solutions.hands
      self.hands = self.mpHands.Hands()
      self.live = 1
      self.handtracking = True
      self.win = win
      self.HandTracking = Button(self.win, text = "Disable Handtracking", command = self.switchHandtracking )
      self.labeler = Label(self.win, width=150)
      self.cap = None
      self.startFeed()

      TurnCameraOn = Button(self.win, text="Start Video", command=self.startFeed)
      TurnCameraOff = Button(self.win, text="Stop Video", command=self.killFeed)
      lambda x : x; TurnCameraOn.pack(side=RIGHT), TurnCameraOff.pack(side=RIGHT), self.HandTracking.pack(side = RIGHT)
      self.labeler.pack()



   def trackHands(self,frame):
      wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]


      if self.handtracking:
            # mpdraw = mp.solutions.drawing_utils
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(cv2image)
            if results.multi_hand_landmarks:
               xl = results.multi_hand_landmarks[0].landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP].x * wCam
               yl = results.multi_hand_landmarks[0].landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP].y * hCam
               pyautogui.moveTo(xl, yl)
               results = cv2image = 0

   def show_feed(self):
            if self.live:
               _, frame = self.cap.read()
               frame = cv2.flip(frame, 1)
               cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               img = Image.fromarray(cv2image)
               if _:
                  opticsControl.trackHands(self,frame)

               imgtk = ImageTk.PhotoImage(image=img)
               self.labeler.imgtk = imgtk
               self.labeler.configure(image=imgtk)
            self.labeler.after(20, self.show_feed)
   def startFeed(self):

         self.killFeed()
         self.live = True
         self.cap = cv2.VideoCapture(0)

         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
         print("Start Feed Works")
         self.show_feed()
   def killFeed(self):
      self.live
      self.live = False
      if self.cap:
         self.cap.release()
   def switchHandtracking(self):

      # Determine is on or off
      if self.handtracking:
         self.HandTracking.config(text= "Activate Handtracking")
         #self.nxtlb.config(text="The Switch is Off")
         self.handtracking = False
      else:

         self.HandTracking.config(text= "Disable Handtracking")
         #self.nxtlb.config(text="The Switch is On")
         self.handtracking = True

instance = Interface()

