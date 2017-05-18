# -*- coding: utf-8 -*-

from config_reader import *
from database_adapter import *
from network_sender import *

sender = NetworkSender()
sender.daemon = True
sender.start()

class Processor:
    def __init__(self):
        self.config = ConfigReader()

        self.connection = None
        self.database = Database()
        self.database.createConnection(self.config.get_db_host(),
                                       self.config.get_db_name(),
                                       self.config.get_db_user(),
                                       self.config.get_db_password(),
                                       port=self.config.get_db_port())

    def init_customer(self, rfid, address):
        customer = self.database.get_single_result('SELECT * FROM em_customer WHERE rfid = %s LIMIT 1' % rfid)
        if customer:
            print address
            balance = customer[2]
            ip_address = address[0]

            # предполагается что считыватель и соответствующее оборудование находятся на одном устройстве
            flowmeters = self.database.get_result(
                " SELECT d.deviceid, d.pinnumber, d.devicetype, d.controllernumber, "
                " d.tubenumber, d.isactive FROM em_device d "
                " JOIN em_controller c ON d.controllernumber = c.number "
                " WHERE c.address = '%s' AND c.isactive = true "
                " AND d.isactive = true AND d.devicetype = 0; " % ip_address)

            valves = self.database.get_result(
                " SELECT d.deviceid, d.pinnumber, d.devicetype, d.controllernumber, "
                " d.tubenumber, d.isactive FROM em_device d "
                " JOIN em_controller c ON d.controllernumber = c.number "
                " WHERE c.address = '%s' AND c.isactive = true "
                " AND d.isactive = true AND d.devicetype = 1; " % ip_address)

            flowmeter_address = (address[0], self.config.get_general_int('FLOWMETER_PORT'))
            sender.send_balance(flowmeter_address, balance)

    def send_prices(self, address):
        ip_address = address[0]

        prices = self.database.get_result(
            " SELECT pinnumber, cost "
            " FROM em_device      em_d "
            " JOIN em_controller  em_c    ON  controllernumber = em_c.number "
            " JOIN em_tube        em_t    ON  tubenumber = em_t.number "
            " JOIN lnk_tubesettings       USING(tubeid) "
            " JOIN em_drink       em_dr   USING(drinkid) "
            " WHERE   address = '%s' "
            " AND     em_d.devicetype = 0 "
            " AND     em_d.isactive = true "
            " AND     em_t.isactive = true "
            " AND     em_t.isactive = true "
            " AND     em_t.isactive = true "
            " AND     em_dr.isactive = true; " % ip_address)

        sender.send_prices(address, prices)
