import pickle
import numpy as np
import struct
import socket
import cv2
import matplotlib.pyplot as plt
import time
host = "0.0.0.0"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)

s.bind((host, port))
s.listen(10)

def service_connection():
    data = bytearray()
    message_size = struct.calcsize("L")
    count = 0
    connection_valid = True

    while True:
        while len(data) < message_size:
            packet = connection.recv(4096)
            if packet == b'': 
                connection_valid = False
                break
            else: 
                data += packet
        
        if connection_valid is False:
            break
        
        data, packed_msg_size = data[message_size:], data[:message_size]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        
        while len(data) < msg_size:            
            packet = connection.recv(4096)
            if packet == b'': 
                connection_valid = False
                break
            else: 
                data += packet
        
        if connection_valid is False:
            break

        data, frame_data = data[msg_size:], data[:msg_size]
        frame = pickle.loads(frame_data)
        yield frame

def bound_frame(frame):
    imgBlur = cv2.GaussianBlur(frame, (7,7), 1)
    gray = cv2.cvtColor(imgBlur,  cv2.COLOR_BGR2GRAY)

    thresh1 =cv2.getTrackbarPos("Thresh1", "Parameters")
    thresh2 =cv2.getTrackbarPos("Thresh2", "Parameters")
    imgCanny = cv2.Canny(gray, thresh1, thresh2)

    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        a = cv2.contourArea(contour)

        min_  = cv2.getTrackbarPos("MinArea", "Parameters")
        max_ = cv2.getTrackbarPos("MaxArea", "Parameters")

        if a > min_ and a < max_:

            cv2.drawContours(frame, contour, -1 ,(0, 255, 255), 7)

            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.1 * peri, True)
            
            if len(approx) < cv2.getTrackbarPos("MaxApprox", "Parameters"):
                x, y, h, w = cv2.boundingRect(approx)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 5)
    
    cv2.imshow("img", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        return

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Thresh1", "Parameters", 244, 255, empty)
cv2.createTrackbar("Thresh2", "Parameters", 255, 255, empty)
cv2.createTrackbar("MinArea", "Parameters", 0, 5000, empty)
cv2.createTrackbar("MaxArea", "Parameters", 0, 5000, empty)
cv2.createTrackbar("MaxApprox", "Parameters", 0, 300, empty)

while True:
    time.sleep(1)
    print(f"Attempting connection ... ")

    try:
        connection, address = s.accept()
        for frame in service_connection():
            print(f"Frame captured ({len(frame)})")

            bound_frame(frame)
            # plt.imshow(frame)
            # plt.show()

    except:
        print(f"Connection Failed ...")
    