import logging
import socket
from util import construct_request as c_req

logger = logging.getLogger("client_log")


# Get the valid RFC number
def get_rfc_number():
    rfc_number = 0
    valid = False
    while not valid:
        try:
            rfc_number = int(input("Enter the required RFC number: "))
            valid = True
        except ValueError:
            logger.error("Error: Please enter an integer for RFC number")

    return rfc_number


# Get the title
def get_rfc_title():
    return input("Enter the title of the RFC (optional): ")


# Validate IP address
def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
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


# Get the add request params
def get_add_lookup_params(command_tokens):
    rfc_number = 0
    title = ""

    if len(command_tokens) == 1:
        # Get the rfc number with the right prompts
        rfc_number = get_rfc_number()
        title = get_rfc_title()

    elif len(command_tokens) >= 2:
        # Check if the entered RFC number is an integer, else get the right one
        try:
            rfc_number = int(command_tokens[1])
        except ValueError:
            # Entered RFC number is not an integer, prompt for the right one
            logger.error("Error: Please enter an integer for RFC number")
            rfc_number = get_rfc_number()

        # If title is entered, set it. Else, get the title
        if len(command_tokens) >= 3:
            title = " ".join(command_tokens[2:len(command_tokens)])
        else:
            title = get_rfc_title()

    return rfc_number, title


# Get the get request params
def get_get_params(command_tokens):
    rfc_number = 0
    peer_ip = ""

    if len(command_tokens) == 1:
        # Get the rfc number with the right prompts
        rfc_number = get_rfc_number()
        peer_ip = get_peer_ip()
    elif len(command_tokens) >= 2:
        try:
            rfc_number = int(command_tokens[1])
        except ValueError:
            # Entered RFC number is not an integer, prompt for the right one
            logger.error("Error: Please enter an integer for RFC number")
            rfc_number = get_rfc_number()

        # If IP entered
        if len(command_tokens) == 3:

            peer_ip = command_tokens[2]
            valid = validate_ip(peer_ip)
            if not valid:
                logger.error("Error: Please enter a valid IP address")
                peer_ip = get_peer_ip()
        else:
            # Get the peer IP
            peer_ip = get_peer_ip()

    else:
        # If more than 3 params passed
        logger.error("Error: Please pass the right number of parameters")

    return rfc_number, peer_ip


# Get add requests
def add_request(command_tokens, client_ip, client_upload_server_port):
    # Check if the other required information is present
    rfc_number, title = get_add_lookup_params(command_tokens)
    logger.debug("Add request params: RFC number: " + str(rfc_number) + ", Title: " + title)

    return c_req.construct_p2s_add_request(str(rfc_number), client_ip, str(client_upload_server_port), title)


# Get get requests
def get_request(command_tokens, client_os):
    # Get the get request parameters
    rfc_number, peer_ip = get_get_params(command_tokens)
    logger.debug("Get request: RFC number: " + str(rfc_number))

    return c_req.construct_p2p_get_request(str(rfc_number), peer_ip, client_os)


# Get list requests
def list_request(client_ip, client_port):
    return c_req.construct_p2s_list_request(client_ip, str(client_port))


# Get lookup requests
def lookup_request(command_tokens, client_ip, client_port):
    # Get the lookup request params
    rfc_number, title = get_add_lookup_params(command_tokens)
    logger.debug("Lookup request params: RFC number: " + str(rfc_number) + ", Title: " + title)

    return c_req.construct_p2s_lookup_request(str(rfc_number), client_ip, str(client_port), title)

