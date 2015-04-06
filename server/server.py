__author__ = 'rg.kavodkar'

import socket
import util.constants as constants

# Assuming the server is running on the same machine
# Needs to be changed when deploying on a different server
host = socket.gethostname()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, constants.SERVER_PORT))

server_socket.listen(5)

while 1:
    client_socket, address = server_socket.accept()
    client_data = str(client_socket.recv(constants.MAX_BUFFER_SIZE), constants.ENCODING)
    print("Client Message:", client_data)
    client_socket.send("Hello World!".encode(constants.ENCODING))
    client_socket.close()


