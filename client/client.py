__author__ = 'rg.kavodkar'
import socket
import logging
import platform
import os
from client import client_logger_init
from client import command_utils
from util import constants
from util import construct_response as c_res


# A function to print the valid command options
def print_help():
    logger.info("  Available commands are:")
    logger.info("  lookup {rfc_number} {title}      # Request to get all the host information that has the given RFC")
    logger.info("  list                             # Request to print the whole index of RFCs from the server")
    logger.info("  help                             # Prints the available command options")
    logger.info("  get {rfc_number} {peer_ip}       # Request to get the RFC from the given host")
    logger.info("  exit                             # Disconnects the client from the server and exits")

# Initialize the client logger
client_logger_init.init()

# Get the OS info
client_os = platform.system() + " " + platform.release()

# TODO: Randomize the port, rather get it from the thread
# Client upload server port number
client_upload_server_port = 43332

# Get the logger object
logger = logging.getLogger("client_log")

# TODO: Remove this
# Get the client hostname
client_hostname = socket.gethostbyname(socket.gethostname())

# TODO: Uncomment
# Get the server hostname
# server_ip = input("Enter the IP address of the server: ")

# Get the location of the RFCs on the local machine
rfc_location = ""
valid = False
while not valid:
    rfc_location = input("Enter the location of the RFCs on the local machine: ")
    valid = os.path.exists(rfc_location)
    if not valid:
        logger.info("Invalid file location. Please enter the correct path.")

# Create a client TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO: Assuming that the server is running on the same machine, needs to be changed
# Connect to the server at the given address
client_socket.connect((client_hostname, constants.SERVER_PORT))

# Get the client socket ip and port
client_ip = client_socket.getsockname()[0]
client_port = client_socket.getsockname()[1]

# Send the hello message to server
hello_str = constants.P2S_HELLO + " " + client_ip + " " + str(client_upload_server_port)
client_socket.send(bytes(hello_str, constants.ENCODING))
message = client_socket.recv(constants.MAX_BUFFER_SIZE)

# Get all the RFCs in the client and send ADD message to the server
rfc_files = os.listdir(rfc_location)

# Add each of the rfc info to the server
for rfc in rfc_files:
    rfc_full_path = os.path.abspath(os.path.join(rfc_location, rfc))
    request_str = command_utils.add_request(rfc_full_path, client_ip, client_upload_server_port)
    client_socket.send(bytes(request_str, constants.ENCODING))

    message = client_socket.recv(constants.MAX_BUFFER_SIZE)
    logger.info("Message from server:\n" + str(message, constants.ENCODING))
# logger.debug("Add request to server\n" + request_str)

# Keep alive connection
while True:
    client_request = input("> ")
    if client_request == constants.CLIENT_CMD_EXIT:
        # Received command for exit, closing the socket
        logger.info("Closing the client socket and the connection")
        client_socket.close()
        break

    # Get the command tokens
    command_tokens = client_request.strip().split(" ")
    command = command_tokens[0]

    # if command is 'help'
    if command == constants.CLIENT_CMD_HELP:
        print_help()
        continue

    # EMPTY
    elif command == "":
        continue

    # If it is one of the command
    else:
        # If the commands are in the list of commands
        if command in constants.CMDS:
            request_str = ""

            # GET
            if command == constants.CLIENT_CMD_GET:
                # Get the get request string
                request_str = command_utils.get_request(client_os)
                logger.debug("Get request to peer\n" + request_str)

            # LIST
            elif command == constants.CLIENT_CMD_LIST:
                # Get the list request string
                request_str = command_utils.list_request(client_ip, client_port)
                logger.debug("List request to server\n" + request_str)

            # LOOKUP
            elif command == constants.CLIENT_CMD_LOOKUP:
                # Get the lookup request string
                request_str = command_utils.lookup_request(client_ip, client_port)
                logger.debug("Lookup request to server\n" + request_str)

            # For all command that are for the server, ie, P2S
            if command != constants.CLIENT_CMD_GET:
                # Send the server the command
                client_socket.send(bytes(request_str, constants.ENCODING))

                # Receive the message from server
                message = client_socket.recv(constants.MAX_BUFFER_SIZE)
                logger.info("Message from server:\n" + str(message, constants.ENCODING))

            # For GET, ie, P2P
            else:
                # TODO: implement the upload server
                logger.info("P2P not implemented yet")
        # For any other 'invalid' commands
        else:
            logger.info("Invalid command. Type 'help' for command options")

