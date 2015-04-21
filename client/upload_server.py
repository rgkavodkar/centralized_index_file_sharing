import socketserver
import logging
import os
from util import utils
from util import constants
from util import parse_request
from util import construct_response as c_res

# Logger object
logger = logging.getLogger(constants.CLIENT_LOG)

# rfc directory location
rfc_location = ""

server = ""


# Function to shutdown the Upload server
def shutdown_server():
    server.shutdown()


# Read RFC data from the file system
def read_rfc_data(rfc_number):
    print("READ RFC %s" % rfc_number)

    try:
        rfc_filename = utils.get_rfc_filename(rfc_number)
        rfc_filename = os.path.abspath(os.path.join(rfc_location, rfc_filename))

        # Get the RFC file stat
        file_stats = os.stat(rfc_filename)
        last_modified = file_stats.st_mtime
        content_length = file_stats.st_size

        # Read the file contents
        rfc_data = utils.read_file(rfc_filename)
    except IOError:
        logger.error("The entered RFC was not found")
        return "", "", ""

    return rfc_data, str(last_modified), str(content_length)


def init(host, port, rfc_loc):
    global server, rfc_location

    # Set the rfc location
    rfc_location = rfc_loc

    # Create an instance of ThreadedUploadServer
    server = ThreadedUploadServer((host, port), RequestHandler)
    logger.info("Starting Upload server at %r:%r" % (host, port))
    server.serve_forever()
    logger.info("Shutting down Upload server")


class RequestHandler(socketserver.BaseRequestHandler):

    # Overriding the method
    def handle(self):

        # Get the connecting host info
        client_host = self.client_address[0].strip()

        served = False

        while not served:
            # Read the request
            request_str = str(self.request.recv(constants.MAX_BUFFER_SIZE), constants.ENCODING).strip()
            response = ""

            # Get the command from the request
            request_command = request_str.split(constants.SPACE)[0]

            # Listen only for GET commands
            if request_command == constants.P2P_GET:
                request_params = parse_request.parse_p2p_get_request(request_str)
                rfc_number = request_params[constants.DICT_RFC_NUMBER]
                rfc_data, last_modified, content_len = read_rfc_data(rfc_number)
                logger.info("Server GET RFC %s request for %s" % (rfc_number, client_host))

                # Construct the response
                if rfc_data == "":
                    response = c_res.construct_p2p_get_response(constants.STATUS_NOT_FOUND[0], constants.STATUS_NOT_FOUND[1],
                                                                utils.get_date(), utils.get_os_info(), last_modified,
                                                                content_len, constants.CONTENT_TYPE_TEXTPLAIN, rfc_data)
                else:
                    response = c_res.construct_p2p_get_response(constants.STATUS_OK[0], constants.STATUS_OK[1],
                                                                utils.get_date(), utils.get_os_info(), last_modified,
                                                                content_len, constants.CONTENT_TYPE_TEXTPLAIN, rfc_data)
                # Set the flag as server since the RFC data is sent
                served = True

            self.request.send(bytes(response, constants.ENCODING))
        logger.info("Terminating the connection with the client")


# An instance of the ThreadedTCPServer class that handles the threading for each client
class ThreadedUploadServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


