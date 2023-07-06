import socket


def main():
    HOST = "0.0.0.0"  # The server's hostname or IP address
    PORT = 8080  # The port used by the server

    print(socket.gethostname())

    mySocket = socket.socket()
    mySocket.bind((HOST, PORT))

    print("After bind")
    mySocket.listen(1)

    print("After listen")
    conn, addr = mySocket.accept()

    print ("Connection from: " + str(addr))
    while True:
            data = conn.recv(1024).decode()
            if not data:
                    break
            print ("from connected  user: " + str(data))

            data = str(data).upper()
            print ("sending: " + str(data))
            conn.send(data.encode())

main()