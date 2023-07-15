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
    cap = cv.VideoCapture(0)

    try:    
        if cap.isOpened(): print("Success fully capturing frame ...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            data = pickle.dumps(frame)
            output_socket.sendall(struct.pack("L", len(data))+data)
            print("Frame Sent!")
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        
        cap.release()
        print(f"Error ... {e}")

        time.sleep(5)
