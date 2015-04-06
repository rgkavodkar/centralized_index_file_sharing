import util.constants as c


# Constructs the GET request in the prescribed format
def construct_p2p_get_request(rfc_number, host, os):
    get_request_string = c.P2P_GET + c.SPACE + c.RFC_TAG + c.SPACE + rfc_number + c.SPACE + c.VERSION + c.CARRIAGE_RETURN + c.LINE_FEED
    get_request_string += c.HOST_TAG + c.SPACE + host + c.CARRIAGE_RETURN + c.LINE_FEED
    get_request_string += c.OS_TAG + c.SPACE + os + c.CARRIAGE_RETURN + c.LINE_FEED
    return get_request_string


# Constructs the ADD request in the prescribed format
def construct_p2s_add_request(rfc_number, host, port, title):
    add_request_string = c.P2S_ADD + c.SPACE + c.RFC_TAG + c.SPACE + rfc_number + c.SPACE + c.VERSION + c.CARRIAGE_RETURN + c.LINE_FEED
    add_request_string += c.HOST_TAG + c.SPACE + host + c.CARRIAGE_RETURN + c.LINE_FEED
    add_request_string += c.PORT_TAG + c.SPACE + port + c.CARRIAGE_RETURN + c.LINE_FEED
    add_request_string += c.TITLE_TAG + c.SPACE + title + c.CARRIAGE_RETURN + c.LINE_FEED
    return add_request_string


# Constructs the LOOKUP request in the prescribed format
def construct_p2s_lookup_request(rfc_number, host, port, title):
    lookup_request_string = c.P2S_LOOKUP + c.SPACE + c.RFC_TAG + c.SPACE + rfc_number + c.SPACE + c.VERSION + c.CARRIAGE_RETURN + c.LINE_FEED
    lookup_request_string += c.HOST_TAG + c.SPACE + host + c.CARRIAGE_RETURN + c.LINE_FEED
    lookup_request_string += c.PORT_TAG + c.SPACE + port + c.CARRIAGE_RETURN + c.LINE_FEED
    lookup_request_string += c.TITLE_TAG + c.SPACE + title + c.CARRIAGE_RETURN + c.LINE_FEED
    return lookup_request_string


# Constructs the LIST request in the prescribed format
def construct_p2s_list_request(host, port):
    list_request_string = c.P2S_LIST + c.SPACE + c.VERSION + c.CARRIAGE_RETURN + c.LINE_FEED
    list_request_string += c.HOST_TAG + c.SPACE + host + c.CARRIAGE_RETURN + c.LINE_FEED
    list_request_string += c.PORT_TAG + c.SPACE + port + c.CARRIAGE_RETURN + c.LINE_FEED
    return list_request_string