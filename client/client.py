__author__ = 'rg.kavodkar'
import socket

host = socket.gethostname()
port = 12345


for i in range(100):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('0.0.0.0', 12600))
    client_socket.connect((host, port))
    message = client_socket.recv(1024)
    print("Received message:", message)
    client_socket.close()