import threading
import tkinter as tk
from tkinter import ttk, StringVar
import numpy as np
import cv2
import socket
import pickle
import struct

class VideoStream:
    obj = None
    root = None
    text = None
    button_stop = None
    status = "Idle..."

    run = False

    thread = None

    host = "localhost"
    port = 2905
    write_socket = None

    image_width = 640
    image_height = 480

    def __init__(self):
    
        # Check camera state
        self.video_cap = cv2.VideoCapture(0)
        VideoStream.run = True if self.video_cap.isOpened() else False

        if VideoStream.run is False:
            VideoStream.update_status("Camera not found ...")
            VideoStream.press_stop()

        else:
            try:
                VideoStream.write_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                VideoStream.write_socket.connect((VideoStream.host, VideoStream.port))
            except ConnectionRefusedError as E:
                VideoStream.update_status("Connection refused ...")
                VideoStream.press_stop()

    def delete(self):
        self.video_cap.release()
        if VideoStream.write_socket is not None:
            VideoStream.write_socket.close()
            VideoStream.write_socket = None

    @classmethod
    def press_stop(cls):

        VideoStream.button_stop.pack_forget()
        VideoStream.button_stop = None
        VideoStream.run = False
        if VideoStream.status == "Transmitted ...":
            VideoStream.thread.join()
            # VideoStream.write_socket.sendall(b"")
            VideoStream.update_status("Stopped Transmitting ...")
            VideoStream.thread = None           
        
        if VideoStream.obj is not None:
            VideoStream.obj.delete()
            del VideoStream.obj
            VideoStream.obj = None

    @classmethod
    def update_status(cls, status):

        if status != VideoStream.status:
            print(f"Status Update: {status}")
            VideoStream.status = status
            VideoStream.text.set(VideoStream.status)

    @classmethod
    def press_start(cls):
        
        # Double clicking start 
        if VideoStream.thread is not None:
            return

        VideoStream.update_status("Starting up ...")

        # Create stop button
        button_stop = tk.Button(VideoStream.root, text="STOP", command=VideoStream.press_stop, bg="red")
        VideoStream.button_stop = button_stop
        button_stop.config(width=35, height=10)
        button_stop.place(x=300 , y=300)
        button_stop.pack(ipadx=5, ipady=5, expand=5)

        # Initilize connection
        VideoStream.obj = VideoStream()

        if VideoStream.status != "Connection refused ...":
            VideoStream.thread = threading.Thread(target=VideoStream.image_capture_thread)
            VideoStream.update_status("Capture started ...")
            VideoStream.thread.start()

    @classmethod
    def image_capture_thread(cls):
        while VideoStream.run is True:
            try:
                return_value , frame = VideoStream.obj.video_cap.read()
            except:
                VideoStream.update_status("Camera closed ...")
                VideoStream.press_stop()
                return
            
            try:
                VideoStream.transmit_frame(frame)
                VideoStream.update_status("Transmitted ...")
            except:
                VideoStream.update_status("Transmission failed ...")
                VideoStream.press_stop()
                return


        VideoStream.obj.video_cap.release()

    @classmethod
    def transmit_frame(cls, frame):
        frame = cv2.resize(frame, (VideoStream.image_width, VideoStream.image_height))
        data = pickle.dumps(frame)
        VideoStream.write_socket.sendall(struct.pack("L", len(data))+data)

root = tk.Tk()
VideoStream.root
root.geometry("800x480")
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