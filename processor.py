# -*- coding: utf-8 -*-

from config_reader import *
from database_adapter import *
from network_sender import *
import select

sender = NetworkSender()
sender.daemon = True
sender.start()


class Processor:
    def __init__(self):
        self.config = ConfigReader()

        self.database = Database()
        self.database.createConnection(self.config.get_db_host(),
                                       self.config.get_db_name(),
                                       self.config.get_db_user(),
                                       self.config.get_db_password(),
                                       port=self.config.get_db_port())

        self.connection = self.database.getConnection()

        curs = self.connection.cursor()
        curs.execute("LISTEN tube_maintenance; ")

    def init_customer(self, rfid, address):
        customer = self.database.get_single_result(
            'SELECT customerid, balance FROM em_customer WHERE rfid = %s LIMIT 1' % rfid)
        if customer:
            balance = customer[1]
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
            sender.send_balance(flowmeter_address, balance, customer[0])

    def send_prices(self, address=None):
        select_query = str(
            " SELECT pinnumber, cost / COALESCE(costvolume, 1.0), isundermaintenance "
            " FROM em_device      em_d "
            " JOIN em_controller  em_c    ON  controllernumber = em_c.number "
            " JOIN em_tube        em_t    ON  tubenumber = em_t.number "
            " JOIN lnk_tubesettings l_ts  USING(tubeid) "
            " JOIN em_drink       em_dr   USING(drinkid) "
            " WHERE   address = '{0}' "
            " AND     em_d.devicetype = 0 "
            " AND     em_d.isactive = true "
            " AND     em_c.isactive = true "
            " AND     em_t.isactive = true "
            " AND     l_ts.isactive = true "
            " AND     em_dr.isactive = true; ")

        if address:
            ip_address = address[0]
            prices = self.database.get_result(select_query.format(ip_address))
            sender.send_prices(address, prices)
        else:
            ip_addresses = self.database.get_result(" SELECT DISTINCT address FROM em_controller; ")
            for single_row in ip_addresses:
                ip_address = single_row[0]
                address = (ip_address, self.config.get_flowmeter_port())
                prices = self.database.get_result(select_query.format(ip_address))
                sender.send_prices(address, prices)

    def register_flow(self, address, message_split):
        pin = message_split[1]
        amount = message_split[2]
        old_balance = message_split[3]
        new_balance = message_split[4]
        customer_id = message_split[5]

        self.database.get_result(
            " UPDATE em_customer SET totalspent = totalspent + balance - {0}, balance = '{0}' "
            " WHERE customerid = '{1}' ".format(new_balance, customer_id)
        )

        ip_address = address[0]

        drink_id = self.database.get_single_result(
            " SELECT drinkid "
            " FROM lnk_tubesettings l_ts "
            " JOIN em_tube 	        em_t    USING (tubeid) "
            " JOIN em_device 	    em_d    ON tubenumber = em_t.number "
            " JOIN em_controller    em_c    ON  controllernumber = em_c.number "
            " JOIN em_drink         em_dr   USING (drinkid) "
            " WHERE em_c.address = '{0}' "
            " AND   em_d.pinnumber = {1} "
            " AND   l_ts.isactive = true "
            " AND   em_t.isactive = true "
            " AND   em_d.isactive = true "
            " AND   em_c.isactive = true; ".format(ip_address, pin)
        )

        if drink_id:
            self.database.get_result(
                " INSERT INTO stat_flowhistory( flowhistoryid, flowtime, drinkid, "
                " amount, spent, customerid, isactive ) "
                " VALUES(uuid_generate_v1mc(), current_timestamp, '{0}', {1}, '{2}', '{3}', 'True'); "
                    .format(drink_id[0], amount, float(old_balance) - float(new_balance), customer_id)
            )

    def check_maintenance(self):
        self.connection.poll()
        while self.connection.notifies:
            notify = self.connection.notifies.pop(0)
            print "Got NOTIFY:", notify.pid, notify.channel, notify.payload
            self.send_prices()
