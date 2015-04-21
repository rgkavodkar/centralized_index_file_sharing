__author__ = 'rg.kavodkar'
import socket
import logging
import os
import threading
from client import client_logger_init
from client import command_utils
from client import upload_server
from util import constants
from util import utils
from util import parse_response as p_res


# A function to print the valid command options
def print_help():
    logger.info("  Available commands are:")
    logger.info("  lookup {rfc_number} {title}      # Request to get all the host information that has the given RFC")
    logger.info("  list                             # Request to print the whole index of RFCs from the server")
    logger.info("  help                             # Prints the available command options")
    logger.info("  get {rfc_number} {peer_ip}       # Request to get the RFC from the given host")
    logger.info("  exit                             # Disconnects the client from the server and exits")


# Get a random open port
def get_open_port():
    # A hacky way to get a random port number
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port

# Initialize the client logger
client_logger_init.init()

# Get the OS info
client_os = utils.get_os_info()

# Get the logger object
logger = logging.getLogger(constants.CLIENT_LOG)

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


# Start the upload server
client_upload_server_port = get_open_port()
logger.info("Available Free port: %r" % client_upload_server_port)
# Call the upload server in a new thread
logger.info("Starting Upload Server thread")
upload_server_thread = threading.Thread(target=upload_server.init, args=(client_hostname, client_upload_server_port, rfc_location, ))
upload_server_thread.start()
logger.info("Started Upload Server thread")

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
response_str = client_socket.recv(constants.MAX_BUFFER_SIZE)

# Get all the RFCs in the client and send ADD message to the server
rfc_files = os.listdir(rfc_location)

# Add each of the rfc info to the server
for rfc in rfc_files:
    rfc_full_path = os.path.abspath(os.path.join(rfc_location, rfc))
    request_str = command_utils.add_request(rfc_full_path, client_ip, client_upload_server_port)
    client_socket.send(bytes(request_str, constants.ENCODING))

    response_str = client_socket.recv(constants.MAX_BUFFER_SIZE)
    logger.info("Message from server:\n" + str(response_str, constants.ENCODING))
# logger.debug("Add request to server\n" + request_str)

# Keep alive connection
while True:
    client_request = input("> ")
    if client_request == constants.CLIENT_CMD_EXIT:
        # Received command for exit, closing the socket
        logger.info("Attempting to close the Upload Server")
        upload_server.shutdown_server()
        logger.info("Closed the Upload Server")
        upload_server_thread.join()
        logger.info("Disconnecting from the Server")
        client_socket.close()
        logger.info("Disconnected from the Server")
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
                request_str, peer_ip, peer_port, rfc_number = command_utils.get_request(client_os)
                logger.info("Get request to peer\n" + request_str)

                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    # Connect to the server at the given address
                    peer_socket.connect((peer_ip, peer_port))

                    # Send the GET message to the peer
                    peer_socket.send(bytes(request_str, constants.ENCODING))

                    # Receive the server data
                    response_str = peer_socket.recv(constants.MAX_BUFFER_SIZE)
                    response_str = str(response_str, constants.ENCODING)

                    # Response parameters
                    response = p_res.parse_p2p_get_response(response_str)

                    # Get the RFC data and write to file
                    rfc_data = response[constants.DICT_RFC_DATA]

                    # Construct the new filename for the RFC
                    new_rfc_file_name = utils.get_rfc_filename(rfc_number)
                    logger.info("1")
                    abs_rfc_file_name = os.path.abspath(os.path.join(rfc_location, new_rfc_file_name))
                    logger.info("2")

                    # Write the RFC file
                    utils.write_file(abs_rfc_file_name, rfc_data)

                    logger.info("Message from server:\n" + response_str)
                except OSError:
                    logger.error("Error: Host %r:%e unreachable" % (peer_ip, peer_port))

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
                response_str = client_socket.recv(constants.MAX_BUFFER_SIZE)
                logger.info("Message from server:\n" + str(response_str, constants.ENCODING))

        # For any other 'invalid' commands
        else:
            logger.info("Invalid command. Type 'help' for command options")

