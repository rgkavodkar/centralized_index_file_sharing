import util.constants as c
import logging

logger = logging.getLogger(c.CLIENT_LOG)


# Constructs the GET response in the prescribed format
def parse_p2p_get_response(response_str):
    # Get individual lines
    lines = response_str.split(c.LINE_FEED)

    # Extract the values from the respective lines
    status = (lines[0].split(c.SPACE)[1], lines[0].split(c.SPACE)[1])
    date = lines[1].split(c.SPACE)[1:len(lines[1])]
    os = lines[2].split(c.SPACE)[2]
    last_modified = lines[3].split(c.SPACE)[1:len(lines[1])]
    content_length = lines[4].split(c.SPACE)[1]
    content_type = lines[5].split(c.SPACE)[1]
    rfc_data = c.LINE_FEED.join(lines[6:len(lines)])

    logger.debug("Parse GET response")
    logger.debug("Status: " + str(status))
    logger.debug("Date: " + str(date))
    logger.debug("OS: " + os)
    logger.debug("Last Modified: " + str(last_modified))
    logger.debug("Content Length: " + str(content_length))
    logger.debug("Content Type: " + content_type)

    request_params = dict()
    request_params[c.DICT_STATUS] = status
    request_params[c.DICT_DATE] = date
    request_params[c.DICT_OS] = os
    request_params[c.DICT_LAST_MODIFIED] = last_modified
    request_params[c.DICT_CONTENT_LENGTH] = content_length
    request_params[c.DICT_CONTENT_TYPE] = content_type
    request_params[c.DICT_RFC_DATA] = rfc_data

    return request_params


# Constructs the LOOKUP response in the prescribed format
def parse_p2s_lookup_response(response_str):
    pass


# Constructs the LIST response in the prescribed format
def parse_p2s_list_response(response_str):
    pass