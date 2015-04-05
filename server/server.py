__author__ = 'rg.kavodkar'

import socket
import time

host = socket.gethostname()
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

server_socket.listen(5)

while 1:
    client_socket, address = server_socket.accept()
    print("Connected to", address)
    client_socket.send("Hello Bro!".encode("utf-8"))
    client_socket.close()


