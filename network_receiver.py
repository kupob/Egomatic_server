# -*- coding: utf-8 -*-

import socket
from threading import *
from collections import deque


class NetworkReceiver(Thread):
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn = None
    addr = None
    server_port = 0

    message_deque = deque([])

    def __init__(self, server_port):
        self.server_port = server_port
        Thread.__init__(self)

    def run(self):
        try:
            self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.cs.bind(('', self.server_port))

            while True:
                message, address = self.cs.recvfrom(1024)
                if message:
                    self.message_deque.append((message, address))

        except socket.error, exc:
            print "Caught exception socket.error : %s" % exc

    def is_message_come(self):
        if not self.message_deque:
            return False
        else:
            return True

    def get_message(self):
        return self.message_deque.popleft()

