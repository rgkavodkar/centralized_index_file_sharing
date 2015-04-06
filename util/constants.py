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
P2S_LIST = "LIST"

P2S_METHODS = {P2S_ADD, P2S_LOOKUP, P2S_LIST}

# Encoding
ENCODING = "utf-8"

# Max Buffer Size
MAX_BUFFER_SIZE = 4096