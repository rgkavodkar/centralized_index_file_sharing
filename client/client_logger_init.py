import logging
import util.constants as constants


# Initialize the logger for the server module
def init():
    # Create the server logger
    client_logger = logging.getLogger("client_log")
    client_logger.setLevel(logging.DEBUG)

    # Create a common formatter
    formatter = logging.Formatter(constants.LOGGING_FORMAT)
    console_formatter = logging.Formatter(constants.LOGGING_FORMAT_CLIENT_CONSOLE)

    # Create a file handler for the log and set level to debug
    file_handler = logging.FileHandler(constants.CLIENT_LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add all the handlers to the logger
    client_logger.addHandler(file_handler)
    client_logger.addHandler(console_handler)

    client_logger.info("Client logger initialized")
