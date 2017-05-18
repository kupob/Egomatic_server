# -*- coding: utf-8 -*-
import socket
# from uuid import getnode as get_mac
from threading import *
from config_reader import *
from collections import deque


class NetworkSender(Thread):
    # mac = get_mac()
    config = ConfigReader()
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message_deque = deque([])

    def run(self):
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cs.bind(('', self.config.get_server_port()))

        while True:
            if self.message_deque:
                queued_message = self.message_deque.popleft()
                address = queued_message[0]
                message = ' '.join(str(x) for x in queued_message[1:])
                try:
                    self.cs.sendto(message, address)
                    print 'Sent ' + str(message) + ' to ' + str(address)
                except socket.error, exc:
                    print exc

    def send_prices(self, address, prices):
        self.message_deque.append([address, self.config.get_message_type('MSG_PRICES'), prices])

    def send_balance(self, address, balance):
        self.message_deque.append([address, self.config.get_message_type('MSG_BALANCE'), balance])
