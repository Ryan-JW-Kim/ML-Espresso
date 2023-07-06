import socket

HOST = "192.168.1.188"  # The server's hostname or IP address
PORT = 8080  # The port used by the server

mySocket = socket.socket()
mySocket.connect((HOST, PORT))

message = input(" -> ")

while message != 'q':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print ('Received from server: ' + data)

        message = input(" -> ")

mySocket.close()