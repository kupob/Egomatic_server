# -*- coding: utf-8 -*-

from database_adapter import *
from config_reader import *
from network_receiver import *
from constants import *

config = ConfigReader()
net_receiver = NetworkReceiver(config.get_server_port())
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

        message_type = int(message_split[1])

        if message_type == config.get_message_type('MSG_RFID'):
            print u'Received RFID from ' + message_split[0] + ' value ' + message_split[2]
            result = database.getResult('SELECT * FROM em_customer WHERE rfid = %s LIMIT 1;' % message_split[2])

            print result
        elif message_type == config.get_message_type('MSG_FLOW'):
            print u'Received flow from ' + message_split[0] + ' pin ' + message_split[2] + ' value ' + message_split[3]
        else:
            print message
