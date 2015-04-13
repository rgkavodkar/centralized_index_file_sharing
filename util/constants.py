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

# Header Tag literals
RFC_TAG = "RFC"
HOST_TAG = "Host:"
OS_TAG = "OS:"
PORT_TAG = "Port:"
TITLE_TAG = "Title:"
DATE_TAG = "Date:"
LAST_MOD_TAG = "Last-Modified:"
CONTENT_LENGTH_TAG = "Content-Length:"
CONTENT_TYPE_TAG = "Content-Type:"

# Status codes
STATUS_OK = (200, "OK")
STATUS_BAD_REQUEST = (400, "Bad Request")
STATUS_NOT_FOUND = (404, "Not Found")
STATUS_VERSION_NOT_SUP = (505, "P2P-CI Version Not Supported")

# Logging constants
LOGGING_FORMAT = "[%(levelname)s] %(asctime)s [%(module)s.%(funcName)s] %(message)s"
SERVER_LOG_FILE = "server.log"
CLIENT_LOG_FILE = "client.log"

# Command Strings
CMD_EXIT = "exit"

# Random Data for Tests
LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et " \
              "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip" \
              " ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore " \
              "eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia " \
              "deserunt mollit anim id est laborum."
