import time
import platform


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
    file = open(file_location, "r")
    return file.read()


# Write file to location
def write_file(abs_file_name, file_content):
    file = open(abs_file_name, "w")
    file.write(file_content)
    file.close()