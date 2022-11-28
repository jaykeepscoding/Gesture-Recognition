import tkinter
from tkinter import *
from PIL import Image, ImageTk
import cv2
import time
import pyautogui
import mediapipe as mp

import pyautogui
import tkinter.ttk as ttk
from tkinter.ttk import *
from ttkthemes import ThemedTk
#from memory_profiler import profile
import numpy as np
pyautogui.PAUSE=0.000

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

   def scrollUp():
      pyautogui.vscroll(10)
      #tkinter.Button(self.win, text="Calibrate").pack()
   def scrollDown():
      pyautogui.vscroll(-10)
   def leftClick():
      pyautogui.leftClick()
class opticsControl():

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
      self.win2 = False

      #self.TurnCameraOn = Button(self.win, text="Start Video", command=self.startFeed)
      self.TurnCameraOff = Button(self.win, text="Settings")
      self.Help = Button(self.win, text="Help", command=self.helpwindow)
      lambda x : x; self.TurnCameraOff.pack(side=RIGHT), self.HandTracking.pack(side = RIGHT), self.Help.pack(side = RIGHT)
      self.labeler.pack()

   def trackHands(self,frame):
      wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]


      if self.handtracking:
            # mpdraw = mp.solutions.drawing_utils
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(cv2image)
            landmark_array = np.empty((0, 2), int)
            if results.multi_hand_landmarks:
               xl = results.multi_hand_landmarks[0].landmark[self.mpHands.HandLandmark.WRIST].x * wCam
               yl = results.multi_hand_landmarks[0].landmark[self.mpHands.HandLandmark.WRIST].y * hCam
               pyautogui.moveTo(xl, yl)
               print(results.multi_hand_landmarks[0])
               
            


   def helpwindow(self):
      if self.win2 == False:

         self.hw = help(self.win.winfo_x(), self.win.winfo_y(),self.win.winfo_width(), self.win.winfo_height())
         self.win2 = True
      else:
         help.close_help(self.hw)
         self.win2 = False
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

         
         self.live = True
         self.cap = cv2.VideoCapture(0)

         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
         print("Start Feed Works")
         self.show_feed()
   def killFeed(self):
      
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

class help(tkinter.Frame):
   def __init__(self, x, y, xoffset, yoffset):
      helpwindow = tkinter.Frame.__init__(self)
      helpwindow = tkinter.Toplevel(self)
      helpwindow.wm_attributes('-toolwindow', 'True')
      helpwindow.wm_attributes('-topmost', 'True')
      width, height = 650, 200

      helpwindow.geometry('%dx%d+%d+%d' % (width, yoffset, x+xoffset+2, y))
      helpwindow.title("Help")

      self.label1 = Label(helpwindow)
      self.button1 = Button(helpwindow).pack(side=RIGHT)
      self.button2 = Button(helpwindow).pack(side=RIGHT)
      self.button3 = Button(helpwindow).pack(side=RIGHT)
      self.button4 = Button(helpwindow).pack(side=RIGHT)
      self.button5 = Button(helpwindow).pack(side=RIGHT)
      self.button6 = Button(helpwindow).pack(side=RIGHT)
      self.label1.pack()
   def close_help(self):
      self.label1.destroy()
      self.destroy()
instance = Interface()

