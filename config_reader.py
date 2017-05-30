# -*- coding: utf-8 -*-

import os.path
import ConfigParser


class ConfigReader:
    class __ConfigReader:
        config_parser = ConfigParser.ConfigParser()

        def __init__(self):
            # self.config_parser.readfp(open())
            self.config_parser.read(['./server_config.ini',  '../config.ini', '../message_types.ini'])

        def get_db_host(self):
            return self.config_parser.get("Database", "DB_HOST")

        def get_db_port(self):
            return self.config_parser.getint("Database", "DB_PORT")

        def get_db_user(self):
            return self.config_parser.get("Database", "DB_USER")

        def get_db_password(self):
            return self.config_parser.get("Database", "DB_PASSWORD")

        def get_db_name(self):
            return self.config_parser.get("Database", "DB_NAME")

        def get_server_port(self):
            return self.config_parser.getint("General", "SERVER_PORT")

        def get_flowmeter_port(self):
            return self.config_parser.getint("General", "FLOWMETER_PORT")

        def get_general(self, field):
            return self.config_parser.get("General", field)

        def get_general_int(self, field):
            return self.config_parser.getint("General", field)

        def get_message_type(self, message_type):
            return self.config_parser.getint("MessageTypes", message_type)

    instance = None

    def __init__(self):
        if not ConfigReader.instance:
            ConfigReader.instance = ConfigReader.__ConfigReader()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)