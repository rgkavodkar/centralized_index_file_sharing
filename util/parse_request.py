import util.constants as c
import logging

logger = logging.getLogger("server_log")

# Constructs the GET request in the prescribed format
def parse_p2p_get_request(request_str):
    pass


# Constructs the ADD request in the prescribed format
def parse_p2s_add_request(request_str):
    # Get individual lines
    lines = request_str.split(c.LINE_FEED)

    # Extract the values from the respective lines
    rfc_number = lines[0].split(c.SPACE)[2]
    host_ip = lines[1].split(c.SPACE)[1]
    host_port = lines[2].split(c.SPACE)[1]
    title_tokens = lines[3].split(c.SPACE)[1:len(lines[3].split(c.SPACE))]
    title = " ".join(title_tokens)
    logger.debug("Parse ADD request")
    logger.debug("RFC Number: " + rfc_number)
    logger.debug("Host IP: " + host_ip)
    logger.debug("Host Port: " + host_port)
    logger.debug("Title: " + title)

    request_params = dict()
    request_params[c.DICT_RFC_NUMBER] = rfc_number
    request_params[c.DICT_IP] = host_ip
    request_params[c.DICT_PORT] = host_port
    request_params[c.DICT_TITLE] = title

    return request_params


# Constructs the LOOKUP request in the prescribed format
def parse_p2s_lookup_request(request_str):
    # Get individual lines
    lines = request_str.split(c.LINE_FEED)

    # Extract the values from the respective lines
    rfc_number = lines[0].split(c.SPACE)[2]
    host_ip = lines[1].split(c.SPACE)[1]
    host_port = lines[2].split(c.SPACE)[1]
    title_tokens = lines[3].split(c.SPACE)[1:len(lines[3].split(c.SPACE))]
    title = " ".join(title_tokens)
    logger.debug("Parse LOOKUP request")
    logger.debug("RFC Number: " + rfc_number)
    logger.debug("Host IP: " + host_ip)
    logger.debug("Host Port: " + host_port)
    logger.debug("Title: " + title)

    request_params = dict()
    request_params[c.DICT_RFC_NUMBER] = rfc_number
    request_params[c.DICT_IP] = host_ip
    request_params[c.DICT_PORT] = host_port
    request_params[c.DICT_TITLE] = title

    return request_params


# Constructs the LIST request in the prescribed format
def parse_p2s_list_request(request_str):
    # Get individual lines
    lines = request_str.split(c.LINE_FEED)

    # Extract the values from the respective lines
    rfc_number = lines[0].split(c.SPACE)[2]
    host_ip = lines[1].split(c.SPACE)[1]
    host_port = lines[2].split(c.SPACE)[1]
    logger.debug("Parse LIST request")
    logger.debug("RFC Number: " + rfc_number)
    logger.debug("Host IP: " + host_ip)
    logger.debug("Host Port: " + host_port)

    request_params = dict()
    request_params[c.DICT_RFC_NUMBER] = rfc_number
    request_params[c.DICT_IP] = host_ip
    request_params[c.DICT_PORT] = host_port

    return request_params