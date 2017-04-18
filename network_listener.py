# -*- coding: utf-8 -*-
import socket
from threading import *
from time import sleep

from config_reader import *

'''
Виды сообщений, передаваемые по сети
0 - передача периодического оповещения
1 - передача стоп-сигнала для клапана
2 - передача данных о расходе со счётчика
'''


class NetworkListener(Thread):
    config = ConfigReader()
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        # self.cs.connect(self.server_address)
        try:
            self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.cs.bind(('', 8800))

            while True:
                message, address = self.cs.recvfrom(1024)
                if message:
                    print address
                    print message

        except socket.error, exc:
            print "Caught exception socket.error : %s" % exc

