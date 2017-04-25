# -*- coding: utf-8 -*-

import os.path


class ConfigReader:
    class __ConfigReader:
        __DB_HOST = ""
        __DB_PORT = 0
        __DB_USER = ""
        __DB_PASSWORD = ""
        __DB_NAME = ""
        __SERVER_PORT = 0
        __MSG_TYPES = {}

        def __init__(self):
            file_name = './settings.conf'

            if os.path.isfile(file_name):
                conf_file = open(file_name, 'r')
                for line in conf_file:
                    if line[0] == '#':
                        continue

                    line_split = line.split()

                    if not line_split:
                        continue

                    code = line_split[0]
                    value = line_split[1]

                    if code == 'DB_HOST':
                        self.__DB_HOST = value
                    elif code == "DB_PORT":
                        self.__DB_PORT = int(value)
                    elif code == "DB_USER":
                        self.__DB_USER = value
                    elif code == "DB_PASSWORD":
                        self.__DB_PASSWORD = value
                    elif code == "DB_NAME":
                        self.__DB_NAME = value
                    elif code == "SERVER_PORT":
                        self.__SERVER_PORT = int(value)
                    elif code[0:4] == "MSG_":
                        self.__MSG_TYPES[code] = int(value)


        def get_db_host(self):
            return self.__DB_HOST

        def get_db_port(self):
            return self.__DB_PORT

        def get_db_user(self):
            return self.__DB_USER

        def get_db_password(self):
            return self.__DB_PASSWORD

        def get_db_name(self):
            return self.__DB_NAME

        def get_server_port(self):
            return self.__SERVER_PORT

        def get_message_type(self, message_type):
            return self.__MSG_TYPES.get(message_type, -1)

    instance = None

    def __init__(self):
        if not ConfigReader.instance:
            ConfigReader.instance = ConfigReader.__ConfigReader()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)