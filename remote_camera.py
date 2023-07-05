import threading
import tkinter as tk
from tkinter import ttk, StringVar
import cv2

class VideoStream:
    obj = None
    root = None
    text = None
    button_stop = None
    status = "Idle..."

    def __init__(self):
    
        self.video_cap = cv2.VideoCapture(0)
        self.run = False

        if self.video_cap.isOpened():
            self.return_val, _ = self.video_cap.read()
            self.run = True
        else:
            self.return_val = False

    @classmethod
    def press_stop(cls):
        VideoStream.update_status("Stopped Transmitting ...")
        VideoStream.obj.run = False
        VideoStream.thread.join()
        VideoStream.button_stop.pack_forget()
        
    @classmethod
    def update_status(cls, status):
        print(f"Status Update: {status}")
        VideoStream.status = status
        VideoStream.text.set(VideoStream.status)

    @classmethod
    def press_start(cls):

        VideoStream.update_status("Starting up ...")
        button_stop = tk.Button(VideoStream.root, text="STOP", command=VideoStream.press_stop, bg="red")
        VideoStream.button_stop = button_stop
        button_stop.config(width=35, height=10)
        button_stop.place(x=300 , y=300)

        button_stop.pack(ipadx=5, ipady=5, expand=5)

        VideoStream.obj = VideoStream()
        VideoStream.thread = threading.Thread(target=VideoStream.image_capture_thread)
        VideoStream.update_status("Capture started ...")
        VideoStream.thread.start()

    @classmethod
    def image_capture_thread(cls):
        while VideoStream.obj.run is True:
            return_value , frame = VideoStream.obj.video_cap.read()
            VideoStream.transmit_frame(frame)

            if VideoStream.status != "Transmitting ..." and VideoStream.obj.run is not False:
                VideoStream.update_status("Transmitting ...")
        VideoStream.obj.video_cap.release()

    @classmethod
    def transmit_frame(cls, frame):
        pass

root = tk.Tk()
VideoStream.root
root.geometry("800x800")
root.title("Test")

VideoStream.text = StringVar()
VideoStream.update_status(VideoStream.status)
status_label = tk.Label(root, textvariable=VideoStream.text)
status_label.pack()

button_start = tk.Button(root, text="START", command=VideoStream.press_start, bg="green")
button_start.config(width=35, height=10)
button_start.place(x=0 , y=0)
button_start.pack(ipadx=5, ipady=5, expand=5)

root.mainloop()