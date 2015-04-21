__author__ = 'rg.kavodkar'

import socket
import socketserver
import logging
import util.constants as constants
import util.parse_request as parse_req
import util.construct_response as construct_response
import util.rfc_info as rfc_object
import util.utils as utils
from server import server_logger_init
from multiprocessing import Lock

# TODO: Make the whole thing like a function

# Initialize the server logger
server_logger_init.init()

# Get the server logger object created in the logger init
logger = logging.getLogger(constants.SERVER_LOG)

# Get the hostname of this machine
host = socket.gethostname()

# Dictionary for holding host's upload server ip and its port
client_info = dict()

# List of rfc to client info
rfc_list = list()


# Add a new client info
def add_client(client_ip, client_port):
    client_info[client_ip] = client_port
    logger.info("Added new client: %s:%s" % (client_ip, client_port))


# Called when an add request is received
def update_on_add(update_params):

    # Extract required info from the dictionary
    rfc_number = update_params[constants.DICT_RFC_NUMBER]
    rfc_title = update_params[constants.DICT_TITLE]
    host_name = update_params[constants.DICT_IP]
    host_port = update_params[constants.DICT_PORT]

    # Get a locking object and acquire it
    lock = Lock()
    lock.acquire()

    try:
        # Update the rfc_list
        rfc_obj = rfc_object.Rfc_info(rfc_number, rfc_title, host_name, host_port)
        rfc_list.append(rfc_obj)
        logger.debug("Added RFC object to list %r" % rfc_obj)
    except:
        logger.error("Failure while updating the rfc info")
    finally:
        lock.release()


# Called when a host disconnects
def remove_on_disconnect(client_ip):
    global rfc_list

    # Get a locking object and acquire it
    lock = Lock()
    lock.acquire()

    try:
        # Keep only those that do not have the hostname parameter as the current client_ip
        rfc_list[:] = [rfc for rfc in rfc_list if not rfc.get_host_name() == client_ip]

        # Remove the client from the client_info dictionary
        client_info.pop(client_ip, None)
        logger.debug("Removed items pertaining to client %s" % client_ip)
    except:
        logger.error("Failure while removing %s's info" % client_ip)
    finally:
        lock.release()


# Search RFC by number
def search_rfc_by_number(rfc_number):
    logger.info("Search for RFC %s" % rfc_number)
    return [rfc for rfc in rfc_list if rfc.get_rfc_number() == rfc_number]


# Search RFC by number
def search_rfc_by_title(rfc_title):
    logger.info("Search for RFC with title: %s" % rfc_title)
    return [rfc for rfc in rfc_list if utils.string_similarity_compare(rfc.get_rfc_title(), rfc_title, constants.SIMILARITY_THRESHOLD)]


# A handler class whose instance is created for each client that connects
class RequestHandler(socketserver.BaseRequestHandler):
    # Overriding the method
    def handle(self):
        client_host = self.client_address[0].strip()
        client_port = self.client_address[1]
        logger.info("Client Connected: " + client_host)
        try:
            while 1:
                # Receive the client request
                client_request_str = str(self.request.recv(constants.MAX_BUFFER_SIZE), constants.ENCODING)

                # If received null, break and close the socket
                if not client_request_str:
                    logger.warn("Closing the connection with " + client_host)
                    break

                # Performing strip after above check to avoid "" as a potential socket terminator
                client_request_str = client_request_str.strip()
                logger.info("Request from client:\n" + client_request_str)

                # Get the command from the request
                request_command = client_request_str.split(constants.SPACE)[0]
                request_params = dict()

                response = ""

                if request_command == constants.P2S_HELLO:
                    logger.info("Received hello string %s " % client_request_str)
                    client_ip = client_request_str.split(" ")[1]
                    client_upload_server_port = client_request_str.split(" ")[2]
                    add_client(client_ip, client_upload_server_port)
                    response = "SUCCESS"

                elif request_command == constants.P2S_ADD:
                    request_params = parse_req.parse_p2s_add_request(client_request_str)
                    update_on_add(request_params)
                    response = "Successfully added the RFC to the server"

                elif request_command == constants.P2S_LIST_STUB:
                    request_params = parse_req.parse_p2s_list_request(client_request_str)

                    # Construct the response with correct status codes
                    status_code = constants.STATUS_NOT_FOUND
                    if len(rfc_list) > 0:
                        status_code = constants.STATUS_OK
                    response = construct_response.construct_p2s_lookup_response(status_code[0], status_code[1], rfc_list)

                elif request_command == constants.P2S_LOOKUP:
                    request_params = parse_req.parse_p2s_lookup_request(client_request_str)
                    rfc_list_subset = list()
                    # Get the corresponding rfcs
                    if request_params[constants.DICT_RFC_NUMBER] == "0":
                        rfc_list_subset = search_rfc_by_title(request_params[constants.DICT_TITLE])
                    else:
                        rfc_list_subset = search_rfc_by_number(request_params[constants.DICT_RFC_NUMBER])

                    # Construct the response with correct status codes
                    status_code = constants.STATUS_NOT_FOUND
                    if len(rfc_list_subset) > 0:
                        status_code = constants.STATUS_OK
                    response = construct_response.construct_p2s_lookup_response(status_code[0], status_code[1], rfc_list_subset)

                # Response for client
                logger.info("Response to client:\n" + response)
                self.request.send(bytes(response, constants.ENCODING))

            logger.info("Client %s Disconnected" % client_host)
        except ConnectionResetError:
            logger.error("Lost connection with client %s" % client_host)
            logger.error("Removing %s data" % client_host)
        except ConnectionError:
            logger.error("Lost connection with client %s" % client_host)
            logger.error("Removing %s data" % client_host)
        finally:
            # Remove all info related to this host
            remove_on_disconnect(client_host)
            logger.debug("Current client_info: " + str(client_info))
            logger.debug("Current rfc_list length: " + str(len(rfc_list)))


# An instance of the ThreadedTCPServer class that handles the threading for each client
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


# Create an instance of ThreadedTCPServer
server = ThreadedTCPServer((host, constants.SERVER_PORT), RequestHandler)
logger.info("Starting main server at %r:%r" % (host, constants.SERVER_PORT))
server.serve_forever()