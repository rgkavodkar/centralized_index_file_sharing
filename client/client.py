__author__ = 'rg.kavodkar'
import socket
import util.constants as constants

host = socket.gethostname()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, constants.SERVER_PORT))
client_socket.send("Hello World!".encode(constants.ENCODING))
message = client_socket.recv(constants.MAX_BUFFER_SIZE)
print("Server message:", str(message, constants.ENCODING))
client_socket.close()