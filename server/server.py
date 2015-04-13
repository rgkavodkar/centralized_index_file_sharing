__author__ = 'rg.kavodkar'

import socket
import socketserver
import util.constants as constants
import logging
from server import server_logger_init

# TODO: Make the whole thing like a function

# Initialize the server logger
server_logger_init.init()

# Get the server logger object created in the logger init
logger = logging.getLogger("server_log")

# Get the hostname of this machine
host = socket.gethostname()


# A handler class whose instance is created for each client that connects
class RequestHandler(socketserver.BaseRequestHandler):
    # Overriding the method
    def handle(self):
        client_host = self.client_address[0]
        client_port = self.client_address[1]
        logger.info("Client Connected: " + client_host)

        while 1:
            # Receive the client request
            client_request = str(self.request.recv(constants.MAX_BUFFER_SIZE), constants.ENCODING)

            # If received null, break and close the socket
            if not client_request:
                logger.warn("Closing the connection with " + client_host)
                break

            # Performing strip after above check to avoid "" as a potential socket terminator
            client_request = client_request.strip()
            logger.info("Request from client: " + client_request)

            # Response for client
            response = client_request.upper()
            logger.info("Response to client: " + response)
            self.request.send(bytes(response, "utf-8"))

        logger.info("Client Disconnected: " + client_host)


# An instance of the ThreadedTCPServer class that handles the threading for each client
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


# Create an instance of ThreadedTCPServer
server = ThreadedTCPServer((host, constants.SERVER_PORT), RequestHandler)
logger.info("Starting main server")
server.serve_forever()