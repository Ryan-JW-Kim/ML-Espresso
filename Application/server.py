import sys
from cluster_manager import Clusters
import pickle
import numpy as np
import struct
import socket
import cv2
import matplotlib.pyplot as plt
import os 
import time
host = "0.0.0.0"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)

s.bind((host, port))
s.listen(10)

def fake_connection():
    files = os.listdir("images")
    while True:
        for file in files:
            # time.sleep(.45)
            with open(f"images\\{file}", "rb") as input:
                yield (file, pickle.load(input))

def save_fake_frame(frame, id):
    with open(f"images\\frame_{id}", "wb") as fh:
        pickle.dump(frame, fh, pickle.HIGHEST_PROTOCOL)
    
def service_connection(connection):
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

    # imgBlur = cv2.GaussianBlur(frame, (7,7), 2)
    # gray = cv2.cvtColor(imgBlur,  cv2.COLOR_BGR2GRAY)

    # thresh1 =cv2.getTrackbarPos("Thresh1", "Parameters")
    # thresh2 =cv2.getTrackbarPos("Thresh2", "Parameters")
    # imgCanny = cv2.Canny(gray, thresh1, thresh2)

    # kernel = np.ones((5,5))
    # imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    # contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    # if not Clusters.start_kmeans:
    #     for contour in contours:
    #         a = cv2.contourArea(contour)
    #         min_  = cv2.getTrackbarPos("MinArea", "Parameters")
    #         max_ = cv2.getTrackbarPos("MaxArea", "Parameters")
    #         # min_ = 0
    #         # max_ = 10000
    #         if a > min_ and a < max_:
    #             cv2.drawContours(frame, contour, -1 ,(0, 255, 255), 7)

    #             if Clusters.all_contours is None:
    #                 Clusters.all_contours = np.array(contour)
            
    #             else:
    #                 if len(Clusters.all_contours) >= Clusters.max_points:
    #                     Clusters.start_kmeans = True
    #                     print("START")
    #                     break
    #                 else:
    #                     print(Clusters.all_contours.shape)
    #                     print(contour.shape)
    #                     Clusters.all_contours = np.append(Clusters.all_contours, contour, axis=0)


    # if Clusters.start_kmeans:
    #     Clusters.all_contours = Clusters.all_contours.reshape((-1, 2))
    #     centroids = Clusters.init_centroids(5)
    #     centroids, indices = Clusters.run_kmeans(Clusters.all_contours, centroids)

    #     for centroid in centroids:
    #         centroid = tuple(np.uint32(centroid))
    #         cv2.circle(frame, centroid, 20, (0, 255, 0), 3)

    cv2.imshow("img", frame)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        return

def empty(a):
    pass

def real_server():
    while True:
        time.sleep(1)
        print(f"Attempting connection ... ")

        try:
            connection, address = s.accept()
            count = 0
            for frame in service_connection(connection):
                save_fake_frame(frame, count)
                count += 1

        except Exception as e:
            print(f"Connection Failed ... {e}")

def test_server():

    frames_consumed = 0
    frame_w, frame_h = None, None
    while True:
        for file, frame in fake_connection():
            
            print(file)
            time.sleep(1)
            bound_frame(frame)

            frames_consumed += 1

if __name__ == "__main__":
    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 640, 240)
    cv2.createTrackbar("Thresh1", "Parameters", 96, 255, empty)
    cv2.createTrackbar("Thresh2", "Parameters", 140, 255, empty)
    cv2.createTrackbar("MinArea", "Parameters", 756, 5000, empty)
    cv2.createTrackbar("MaxArea", "Parameters", 2277, 5000, empty)
    cv2.createTrackbar("MaxApprox", "Parameters", 0, 300, empty)
    test_server()
    # real_server()