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
server_ip = command_utils.get_peer_ip()

# Get the location of the RFCs on the local machine
rfc_location = ""
valid = False
while not valid:
    rfc_location = input("Enter the location of the RFCs on the local machine: ")
    valid = os.path.exists(rfc_location)
    if not valid:
        print("Invalid file location. Please enter the correct path.")
        logger.debug("Invalid file location. Please enter the correct path.")


# Start the upload server
client_upload_server_port = get_open_port()
logger.debug("Available Free port: %r" % client_upload_server_port)
# Call the upload server in a new thread
logger.debug("Starting Upload Server thread")
upload_server_thread = threading.Thread(target=upload_server.init, args=(client_hostname, client_upload_server_port, rfc_location, ))
upload_server_thread.start()
logger.debug("Started Upload Server thread")

# Create a client TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server at the given address
client_socket.connect((server_ip, constants.SERVER_PORT))

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

    # TODO: Show correct message to client
    response_str = client_socket.recv(constants.MAX_BUFFER_SIZE)
    logger.debug("Message from server:\n" + str(response_str, constants.ENCODING))

# Keep alive connection
while True:
    client_request = input("> ")
    if client_request == constants.CLIENT_CMD_EXIT:
        # Received command for exit, closing the socket
        upload_server.shutdown_server()
        upload_server_thread.join()
        logger.info("Disconnecting from the Server")
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
                request_str, peer_ip, peer_port, rfc_number = command_utils.get_request(client_os)
                logger.debug("Get request to peer\n" + request_str)

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
                    abs_rfc_file_name = os.path.abspath(os.path.join(rfc_location, new_rfc_file_name))

                    # Write the RFC file
                    utils.write_file(abs_rfc_file_name, rfc_data)
                    logger.debug("Message from server:\n" + response_str)
                    print("Successfully downloaded RFC from the %s" % peer_ip)

                    request_str = command_utils.add_request(abs_rfc_file_name, client_ip, client_upload_server_port)
                    client_socket.send(bytes(request_str, constants.ENCODING))

                    response_str = client_socket.recv(constants.MAX_BUFFER_SIZE)
                    logger.debug("Message from server:\n" + str(response_str, constants.ENCODING))

                except OSError:
                    logger.error("Error: Host %r:%e unreachable" % (peer_ip, peer_port))

            # LIST
            elif command == constants.CLIENT_CMD_LIST:
                # Get the list request string
                request_str = command_utils.list_request(client_ip, client_port)
                logger.debug("List request to server\n" + request_str)

                # Send the server the command
                client_socket.send(bytes(request_str, constants.ENCODING))

                # Receive the message from server
                response_str = str(client_socket.recv(constants.MAX_BUFFER_SIZE), constants.ENCODING)
                logger.debug("Message from server:\n" + response_str)

                # Extract the response
                response = p_res.parse_p2s_list_response(response_str)
                print(response)

            # LOOKUP
            elif command == constants.CLIENT_CMD_LOOKUP:
                # Get the lookup request string
                request_str = command_utils.lookup_request(client_ip, client_port)
                logger.debug("Lookup request to server\n" + request_str)

                # Send the server the command
                client_socket.send(bytes(request_str, constants.ENCODING))

                # Receive the message from server
                response_str = str(client_socket.recv(constants.MAX_BUFFER_SIZE), constants.ENCODING)
                logger.debug("Message from server:\n" + response_str)

                # Extract the response
                response = p_res.parse_p2s_lookup_response(response_str)
                print(response)

        # For any other 'invalid' commands
        else:
            print("Invalid command. Type 'help' for command options")
            logger.debug("Invalid command. Type 'help' for command options")

print("Good Bye!")