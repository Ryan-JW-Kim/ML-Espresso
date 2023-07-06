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
        print(f"FRAME ({count})")    
        count += 1
        plt.imshow(frame)
        plt.show()

while True:
    time.sleep(1)
    print(f"Attempting connection ... ")

    try:
        connection, address = s.accept()
        service_connection()
    
    except:
        print(f"Connection Failed ...")
    