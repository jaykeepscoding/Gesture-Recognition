import inspect
import tkinter as tk
import cv2
from PIL import Image,ImageTk




class base(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        

        btn = tk.Button(self, text="Stop Feed")
        btn2 = tk.Button(self, text="Start Feed")
        btn3 = tk.Button(self, text="Calibrate")
        btn4 = tk.Button(self, text="Help")
        btns = [btn.pack(side=tk.RIGHT), btn2.pack(side=tk.RIGHT), btn3.pack(side=tk.RIGHT), btn4.pack(side=tk.RIGHT)]

        lambda x : x; btns
        #a = tk.Label(width=50, height=10, bg="gray").pack()
        label =tk.Label(root)
        label.pack()
        cap= cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,150)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,200)
        # Define function to show frame
        def show_frames():
            # Get the latest frame and convert into Image
            cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            # Convert image to PhotoImage
            imgtk = ImageTk.PhotoImage(image = img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            # Repeat after an interval to capture continiously
            label.after(20, show_frames)

        show_frames()

        self.pack()


root = tk.Tk()
root.title("Gesture Recognition")
root.wm_attributes('-toolwindow', 'True')


tst = base(root)
tst.mainloop()
