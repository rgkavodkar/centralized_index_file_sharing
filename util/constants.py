"""
This file holds the constants used across the project
"""

# Port on which the CI server is listening
SERVER_PORT = 7734

# Constant for the method name for P2P Get
P2P_GET = "GET"

# Constants for the P2S methods
P2S_ADD = "ADD"
P2S_LOOKUP = "LOOKUP"
P2S_LIST = "LIST ALL"

P2S_METHODS = {P2S_ADD, P2S_LOOKUP, P2S_LIST}

# Encoding
ENCODING = "utf-8"

# Max Buffer Size
MAX_BUFFER_SIZE = 4096

# Version String
VERSION = "P2P-CI/1.0"

# String literal constants
CARRIAGE_RETURN = "\r"
LINE_FEED = "\n"
SPACE = " "

# RFC tag literal
RFC_TAG = "RFC"
HOST_TAG = "Host:"
OS_TAG = "OS:"
PORT_TAG = "Port:"
TITLE_TAG = "Title:"

# Status codes
STATUS_OK = (200, "OK")
STATUS_BAD_REQUEST = (400, "Bad Request")
STATUS_NOT_FOUND = (404, "Not Found")
STATUS_VERSION_NOT_SUP = (505, "P2P-CI Version Not Supported")