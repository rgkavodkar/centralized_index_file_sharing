

class Rfc_info():

    def __init__(self, rfc_number, rfc_title, host_name, host_port):
        self.__rfc_number = rfc_number
        self.__rfc_title = rfc_title
        self.__host_name = host_name
        self.__host_port = host_port

    def get_rfc_number(self):
        return self.__rfc_number

    def get_rfc_title(self):
        return self.__rfc_title

    def get_host_name(self):
        return self.__host_name

    def get_host_port(self):
        return self.__host_port
