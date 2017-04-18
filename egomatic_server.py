# -*- coding: utf-8 -*-

from database_adapter import *
from config_reader import *
from network_listener import *

config = ConfigReader()
listener = NetworkListener()
listener.start()

database = Database()
database.createConnection(config.get_db_host(), 'egomatic', config.get_db_user(), config.get_db_password(), port=config.get_db_port())

beers = database.getResult('SELECT * FROM em_drink;')

# TODO keyboard listener