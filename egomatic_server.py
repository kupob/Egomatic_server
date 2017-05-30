# -*- coding: utf-8 -*-

from config_reader import *
from network_receiver import *
from processor import *
import time

config = ConfigReader()
net_receiver = NetworkReceiver(config.get_server_port())
net_receiver.daemon = True
net_receiver.start()

processor = Processor()

check_maintenance_time = 0
# main loop
while True:

    while net_receiver.is_message_come():
        message_and_address = net_receiver.get_message()
        message = message_and_address[0]
        address = message_and_address[1]
        print address
        message_split = message.split()

        message_type = int(message_split[0])

        if message_type == config.get_message_type('MSG_RFID'):
            print u'Received RFID from ' + str(address) + ' value ' + message_split[1]
            processor.init_customer(message_split[1], address)
        elif message_type == config.get_message_type('MSG_FLOW'):
            print u'Received flow from ' + str(address) + ' pin ' + message_split[1] + ' value ' + message_split[2]
            print u'New customer balance is ' + message_split[3]
            if message_split[4]:
                processor.register_flow(address, message_split)
        elif message_type == config.get_message_type('MSG_PRICES_REQUEST'):
            print u'Received price request from ' + str(address)
            processor.send_prices(address)
        else:
            print 'Recv ' + message

    if time.time() * 1000 - check_maintenance_time > 1000:
        check_maintenance_time = time.time() * 1000
        processor.check_maintenance()
