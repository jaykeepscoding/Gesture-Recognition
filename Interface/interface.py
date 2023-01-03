import tkinter
from tkinter import *
from PIL import Image, ImageTk
import cv2
import time
import pyautogui
import mediapipe as mp
import tensorflow as tf
import pyautogui
import tkinter.ttk as ttk
from tkinter.ttk import *
from ttkthemes import ThemedTk
import numpy as np
#Removes a pyautogui safety feature 
pyautogui.PAUSE=0.000

class Interface():
   """
   Initializes a window with a stylized tkinter model
   Sets standard window attributes
   Makes Main Window non-resizable
   Calls Optics Control
   Loops Tkinter application
   """
   def __init__(self):
      self.win = Tk()
      s = ttk.Style()
      s.theme_use('xpnative')
      self.win.title("Gesture Interface")
      self.win.wm_attributes('-toolwindow', 'True')
      self.win.wm_attributes('-topmost', 'True')
      #self.win.wm_attributes('-topmost', 'False')
      self.win.resizable(0,0)
      opticsControl(self.win)
      self.win.mainloop()

class opticsControl():
   """
   Initializes Mediapipe Model, and our Model
   Defines parameters for how Mediapipe should treat hands
   Provides initial values for: Live, HandTracking, capture, and Secondary Window
   Creates a button to disable Hand Tracking
   Creates simple labels for main windows
   """
   def __init__(self, win):
      self.mpHands = mp.solutions.hands
      self.hands = self.mpHands.Hands(max_num_hands=1,min_detection_confidence=0.35, min_tracking_confidence=0.9 )
      self.live = 1
      self.handtracking = False
      self.win = win
      self.HandTracking = Button(self.win, text = "Activate Handtracking", command = self.switchHandtracking )
      self.labeler = Label(self.win, width=150)
      self.cap = None
      self.startFeed()
      self.win2 = False
      self.model = tf.keras.models.load_model("Interface/keypoint_classifier.hdf5")
      self.Help = Button(self.win, text="Help", command=self.helpwindow)
      lambda x : x; self.HandTracking.pack(side = RIGHT), self.Help.pack(side = RIGHT)
      self.labeler.pack()
   """
   Grabs Screen Dimensions
   As hand is being tracked/detected by Mediapipe
   The image is processed and translated into a readable set of landmarks
   The landmarks are compiled in order into a list of coordinates (normalized from camera feed)
   This array of landmarks is fed to the prediction model and generates a number between 0-8
   A relative X and relative Y are then used to map hand movements to cursor movements if the detected gesture happens to be 8 (a closed palm)
   A if else statement follows for actions to be performed on detection of each gesture 
   """
   def trackHands(self,frame):
      wCam, hCam = pyautogui.size()[0], pyautogui.size()[1]
      if self.handtracking:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(cv2image)
            if results.multi_hand_landmarks:
               hand_pos = [[]]
               fingers = [self.mpHands.HandLandmark.THUMB_TIP, self.mpHands.HandLandmark.INDEX_FINGER_TIP, self.mpHands.HandLandmark.MIDDLE_FINGER_TIP, self.mpHands.HandLandmark.RING_FINGER_TIP, self.mpHands.HandLandmark.PINKY_TIP]
               for v in fingers:
                  xl = results.multi_hand_world_landmarks[0].landmark[v].x
                  yl = results.multi_hand_world_landmarks[0].landmark[v].y
                  if v in fingers:
                     hand_pos[0].append(xl)
                     hand_pos[0].append(yl)
               test = self.model.predict(np.array(hand_pos))
               tst1 = np.argmax(test)
               xr = results.multi_hand_landmarks[0].landmark[self.mpHands.HandLandmark.PINKY_MCP].x * wCam
               yr = results.multi_hand_landmarks[0].landmark[self.mpHands.HandLandmark.MIDDLE_FINGER_PIP].y * hCam
               if tst1 == 0:
                  pyautogui.leftClick()
                  time.sleep(.2)
               elif tst1 == 1:
                  pyautogui.rightClick()
                  time.sleep(.1)
               elif tst1 == 2:
                  pyautogui.scroll(-10)
               elif tst1 == 3:
                  pyautogui.hotkey('left')
                  #time.sleep(0.1)
                  #pyautogui.hscroll(-10)
               elif tst1 == 4:
                  pyautogui.hotkey('right')
                  #pyautogui.hscroll(10)
               elif tst1 == 5:
                  pyautogui.scroll(10)
               elif tst1 == 6:
                  pyautogui.keyDown('ctrl')
                  pyautogui.scroll(10)
                  pyautogui.keyUp('ctrl')
                  time.sleep(.1)
               elif tst1 == 7:
                  pyautogui.keyDown('ctrl')
                  pyautogui.scroll(-10)
                  pyautogui.keyUp('ctrl')
                  time.sleep(.1)
               elif tst1 == 8:
                  pyautogui.moveTo(xr, yr)
               return 0

   #Closable Help Window Call
   def helpwindow(self):
      if self.win2 == False:
         self.hw = help(self.win.winfo_x(), self.win.winfo_y(),self.win.winfo_width(), self.win.winfo_height())
         self.win2 = True
      else:
         help.close_help(self.hw)
         self.win2 = False
   #Live image processing and refreshing
   def show_feed(self):
            if self.live:
               _, frame = self.cap.read()
               frame = cv2.flip(frame, 1)
               cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               img = Image.fromarray(cv2image)
               
               if _:
                  opticsControl.trackHands(self,frame)
               img = img.resize((213,120), resample = Image.Resampling.BILINEAR)
               imgtk = ImageTk.PhotoImage(image=img)
               self.labeler.imgtk = imgtk
               self.labeler.configure(image=imgtk)
            self.labeler.after(10, self.show_feed)
   #Start camera feed and Call show_feed
   def startFeed(self):   
         self.live = True
         self.cap = cv2.VideoCapture(0)
         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
         print("Start Feed Works")
         self.show_feed()

   def switchHandtracking(self):
      # Determine is on or off
      if self.handtracking:
         self.HandTracking.config(text= "Activate Handtracking")
         self.handtracking = False
      else:
         self.HandTracking.config(text= "Disable Handtracking")
         self.handtracking = True
   """
   Simple help window
   Creates itself and is destoyed on command
   """
class help(tkinter.Frame):
   def __init__(self, x, y, xoffset, yoffset):
      helpwindow = tkinter.Frame.__init__(self)
      helpwindow = tkinter.Toplevel(self)
      helpwindow.wm_attributes('-toolwindow', 'True')
      helpwindow.wm_attributes('-topmost', 'True')
      helpwindow.resizable(0,0)
      width, height = 340, 600
      helpwindow.geometry('%dx%d+%d+%d' % (width, yoffset+735, x+xoffset+2, y))
      helpwindow.title("Help")
      self.img = ImageTk.PhotoImage(Image.open("Interface/table.png"))
      self.label1 = Label(helpwindow, image=self.img)
      self.label1.pack()
   def close_help(self):
      self.label1.destroy()
      self.destroy()
instance = Interface()

