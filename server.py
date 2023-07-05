import pickle
import numpy as np
import struct
import socket
import cv2
import matplotlib.pyplot as plt

host = ""
port = 2905

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))
s.listen(10)

connection, address = s.accept()
data = bytearray()
message_size = struct.calcsize("L")

while True:

    while len(data) < message_size:
        data += connection.recv(4096)

    packed_msg_size = data[:message_size]
    data = data[message_size:]

    msg_size = struct.unpack("L", packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += connection.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    
    frame = pickle.loads(frame_data)
    plt.imshow(frame)

    