import numpy as np
import cv2 as cv
import socket
import time
import pickle
import struct
import cv2

host = "192.168.1.188"
port = 8080

while True:
    output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output_socket.connect((host, port))
    print(f"Connection Established ...")

    try:    
        cap = cv.VideoCapture(0)

        if cap.isOpened(): print("Success fully capturing frame ...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            data = pickle.dumps(frame)
            output_socket.sendall(struct.pack("L", len(data))+data)

        cap.release()

    except Exception as e:

        print(f"Error ... {e}")
        time.sleep(5)
