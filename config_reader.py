# -*- coding: utf-8 -*-

import os.path


class ConfigReader:
    class __ConfigReader:
        __DB_HOST = ""
        __DB_PORT = 0
        __DB_USER = ""
        __DB_PASSWORD = ""

        def __init__(self):
            file_name = './db_settings.conf'

            if os.path.isfile(file_name):
                conf_file = open(file_name, 'r')
                for line in conf_file:
                    if line[0] == '#':
                        continue

                    line_split = line.split()
                    if not line_split:
                        continue
                    if line_split[0] == 'DB_HOST':
                        self.__DB_HOST = line_split[1]
                    elif line_split[0] == "DB_PORT":
                        self.__DB_PORT = int(line_split[1])
                    elif line_split[0] == "DB_USER":
                        self.__DB_USER = line_split[1]
                    elif line_split[0] == "DB_PASSWORD":
                        self.__DB_PASSWORD = line_split[1]

        def get_db_host(self):
            return self.__DB_HOST

        def get_db_port(self):
            return self.__DB_PORT

        def get_db_user(self):
            return self.__DB_USER

        def get_db_password(self):
            return self.__DB_PASSWORD

    instance = None

    def __init__(self):
        if not ConfigReader.instance:
            ConfigReader.instance = ConfigReader.__ConfigReader()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)