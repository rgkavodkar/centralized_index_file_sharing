import time
import platform
from difflib import SequenceMatcher


# Get current time and data
def get_date():
    return time.strftime("%c")


# Get system OS info
def get_os_info():
    return platform.system() + " " + platform.release()


# Get RFC filename by number
def get_rfc_filename(rfc_number):
    return "rfc" + str(rfc_number) + ".txt"


# Read a file
def read_file(file_location):
    # Open file in 'r' mode for reading
    file = open(file_location, "r")
    return file.read()


# Write file to location
def write_file(abs_file_name, file_content):
    # Open file in 'w' mode for writing
    file = open(abs_file_name, "w")
    file.write(file_content)
    file.close()


# String similarity compare
def string_similarity_compare(string_1, string_2, ratio):
    # Convert the two string into tokens and sort them and reconstruct a string
    tokens_1 = ''.join(e for e in string_1 if e.isalnum() or e == " ")
    tokens_1 = sorted(tokens_1.split(" "))
    tokens_1 = " ".join(tokens_1)
    tokens_2 = ''.join(e for e in string_2 if e.isalnum() or e == " ")
    tokens_2 = sorted(tokens_2.split(" "))
    tokens_2 = " ".join(tokens_2)

    # Check the similarity between the two strings
    similarity_ratio = SequenceMatcher(None, tokens_1, tokens_2).ratio()

    # If similarity ratio is acceptable, send True
    if similarity_ratio >= ratio:
        return True
    else:
        return False