import logging
import util.constants as constants


# Initialize the logger for the server module
def init():
    # Create the server logger
    server_logger = logging.getLogger("server_log")
    server_logger.setLevel(logging.INFO)

    # Create a common formatter
    formatter = logging.Formatter(constants.LOGGING_FORMAT)

    # Create a file handler for the log and set level to debug
    file_handler = logging.FileHandler(constants.SERVER_LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add all the handlers to the logger
    server_logger.addHandler(file_handler)
    server_logger.addHandler(console_handler)

    server_logger.info("Server logger initialized")
