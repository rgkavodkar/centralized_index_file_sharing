import util.constants as c


# Constructs the GET response in the prescribed format
def construct_p2p_get_response(status_code, status_phrase, date, os, last_modified, content_length, content_type, data):
    get_response_string = c.VERSION + c.SPACE + status_code + c.SPACE + status_phrase+ c.CARRIAGE_RETURN + c.LINE_FEED
    get_response_string += c.DATE_TAG + c.SPACE + date + c.CARRIAGE_RETURN + c.LINE_FEED
    get_response_string += c.OS_TAG + c.SPACE + os + c.CARRIAGE_RETURN + c.LINE_FEED
    get_response_string += c.LAST_MOD_TAG + c.SPACE + last_modified + c.CARRIAGE_RETURN + c.LINE_FEED
    get_response_string += c.CONTENT_LENGTH_TAG + c.SPACE + content_length + c.CARRIAGE_RETURN + c.LINE_FEED
    get_response_string += c.CONTENT_TYPE_TAG + c.SPACE + content_type + c.CARRIAGE_RETURN + c.LINE_FEED
    get_response_string += data
    return get_response_string


# Constructs the LOOKUP response in the prescribed format
def construct_p2s_lookup_response(status_code, status_phrase, rfc_list):
    return construct_p2s_list_response(status_code, status_phrase, rfc_list)


# Constructs the LIST response in the prescribed format
def construct_p2s_list_response(status_code, status_phrase, rfc_list):
    list_response_string = c.VERSION + c.SPACE + status_code + c.SPACE + status_phrase+ c.CARRIAGE_RETURN + c.LINE_FEED
    # Care should be taken for using the correct type cast
    for rfc in rfc_list:
        list_response_string += rfc.get_rfc_number() + c.SPACE + rfc.get_rfc_title() + c.SPACE + rfc.get_host_name()\
            + c.SPACE + rfc.get_host_port() + c.CARRIAGE_RETURN + c.LINE_FEED
    list_response_string += c.CARRIAGE_RETURN + c.LINE_FEED
    return list_response_string
