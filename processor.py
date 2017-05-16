# -*- coding: utf-8 -*-

from config_reader import *
from database_adapter import *
# import ConfigParser


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
            balance = customer[2]
            ip_address = address[0]

            flowmeters = self.database.get_result(" SELECT d.deviceid, d.pinnumber, d.devicetype, d.controllernumber, "
                                                  " d.tubenumber, d.isactive FROM em_device d "
                                                  " JOIN em_controller c ON d.controllernumber = c.number "
                                                  " WHERE c.address = '%s' AND c.isactive = true "
                                                  " AND d.isactive = true AND d.devicetype = 0; " % ip_address)

            valves = self.database.get_result("SELECT d.deviceid, d.pinnumber, d.devicetype, d.controllernumber, "
                                              " d.tubenumber, d.isactive FROM em_device d "
                                              " JOIN em_controller c ON d.controllernumber = c.number "
                                              " WHERE c.address = '%s' AND c.isactive = true "
                                              " AND d.isactive = true AND d.devicetype = 1; " % ip_address)
            print flowmeters
            print valves
