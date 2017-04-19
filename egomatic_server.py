# -*- coding: utf-8 -*-

from database_adapter import *
from config_reader import *
from network_receiver import *
from constants import *

config = ConfigReader()
net_receiver = NetworkReceiver()
net_receiver.daemon = True
net_receiver.start()

database = Database()
database.createConnection(config.get_db_host(),
                          config.get_db_name(),
                          config.get_db_user(),
                          config.get_db_password(),
                          port=config.get_db_port())

# main loop
while True:

    while net_receiver.is_message_come():
        message = net_receiver.get_message()
        message_split = message.split()

        if message_split[1] == MSG_FLOW:
            print u'Received flow from ' + message_split[0] + ' pin ' + message_split[2] + ' value ' + message_split[3]
        else:
            print message
