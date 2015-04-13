__author__ = 'rg.kavodkar'
import socket
import util.constants as constants
import logging
from client import client_logger_init

# TODO: Put the whole functionality into a function

# Initialize the client logger
client_logger_init.init()

# Get the logger object
logger = logging.getLogger("client_log")

# Get the client hostname
host = socket.gethostname()

# Create a client TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO: Assuming that the server is running on the same machine, needs to be changed
# Connect to the server at the given address
client_socket.connect((host, constants.SERVER_PORT))

# Keep alive connection
while True:
    client_request = input("Enter Command: ")
    if client_request == constants.CMD_EXIT:
        # Received command for exit, closing the socket
        logger.info("Closing the client socket and the connection")
        client_socket.close()
        break

    # Send the server the command
    client_socket.send(bytes(client_request, constants.ENCODING))
    logger.info("Request to server: " + client_request)
    # Receive the message from server
    message = client_socket.recv(constants.MAX_BUFFER_SIZE)
    logger.info("Message from server: " + str(message, constants.ENCODING))