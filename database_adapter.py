# -*- coding: utf-8 -*-
import sys
# import psycopg2
from psycopg2 import *
# from psycopg2 import extras as _extras

'''
class Database:
    def __init__(self):
        self.connection = None

    def createConnection(self, hostName, dataBaseName, login, password, port=None):
        try:
            # log.printlog(u'Попытка соединения с БД %s : %s' % (hostName, dataBaseName), u"INFO")
            self.connection = psycopg2.connect(
                host=hostName,
                database=dataBaseName,
                user=login,
                password=password,
                port=port)

            # if port:
            # log.printlog(u'Подключились %s/%s : %s' % (hostName, port, dataBaseName), u"INFO")
            # else:
            # log.printlog(u'Подключились %s : %s' % (hostName, dataBaseName), u"INFO")

        except psycopg2.DatabaseError, e:
            # log.printlog(u'Ошибка подключения к базе данных %s' % str(e), u"ERROR")
            sys.exit(-1)

    def getConnection(self):
        return self.connection

    def closeConnection(self):
        if self.connection:
            self.connection.close()

    def getResult(self, select, parameters=None):
        cursor = self.connection.cursor(cursor_factory=_extras.DictCursor)
        # Если переданы параметры, запрос выполняется с параметрами
        if parameters:
            cursor.execute(select, parameters)
        else:
            cursor.execute(select)
        return cursor.fetchall()
'''