import logging
import socket
from util import construct_request as c_req

logger = logging.getLogger("client_log")


# Get the valid RFC number
def get_rfc_number(empty_allowed=False):
    rfc_number = 0
    valid = False
    while not valid:
        try:
            rfc_number_input = input("Enter the required RFC number: ")
            if rfc_number_input != "" or not empty_allowed:
                rfc_number = int(rfc_number_input)
            valid = True
        except ValueError:
            logger.error("Error: Please enter an integer for RFC number")

    return rfc_number


# Get the title
def get_rfc_title():
    return input("Enter the title of the RFC: ")


# Validate IP address
def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        if len(ip.split(".")) == 4:
            return True
        return False
    except socket.error:
        return False


# Get the peer ip
def get_peer_ip():
    peer_ip = ""
    valid = False
    while not valid:
        peer_ip = input("Enter the IP of the peer: ")
        valid = validate_ip(peer_ip)
        if not valid:
            logger.error("Error: Please enter a valid IP address")

    return peer_ip


# Get the ADD request params from file location
def get_add_params(file_location):
    from random import randint
    random_int = randint(0, 1009)
    return random_int, "hello world"


# Get add requests
def add_request(file_location, client_ip, client_upload_server_port):
    # Check if the other required information is present
    rfc_number, title = get_add_params(file_location)

    logger.debug("Add request params: RFC number: " + str(rfc_number) + ", Title: " + title)

    return c_req.construct_p2s_add_request(str(rfc_number), client_ip, str(client_upload_server_port), title)


# Get get requests
def get_request(client_os):
    # Get the rfc_number and the peer_ip
    rfc_number = get_rfc_number()
    peer_ip = get_peer_ip()

    logger.debug("Get request: RFC number: " + str(rfc_number))

    return c_req.construct_p2p_get_request(str(rfc_number), peer_ip, client_os)


# Get list requests
def list_request(client_ip, client_port):
    return c_req.construct_p2s_list_request(client_ip, str(client_port))


# Get lookup requests
def lookup_request(client_ip, client_port):
    # Get the rfc_number and the title

    valid = False

    while not valid:
        rfc_number = get_rfc_number(empty_allowed=True)
        title = get_rfc_title()
        if rfc_number == 0 and title == "":
            logger.error("Error: Both RFC number and title cannot be empty. Please reenter")
        else:
            valid = True

    logger.debug("Lookup request params: RFC number: " + str(rfc_number) + ", Title: " + title)

    return c_req.construct_p2s_lookup_request(str(rfc_number), client_ip, str(client_port), title)

