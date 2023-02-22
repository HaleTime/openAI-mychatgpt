import configparser

import mysql.connector

config = configparser.ConfigParser()
config.read('dbconfig.ini')

# 获取配置文件中的值
database = 'xiaobaimao'
host = config.get(database, 'host')
port = config.getint(database, 'port')
user = config.get(database, 'username')
password = config.get(database, 'password')


# config = {
#     'user': user,
#     'password': password,
#     'host': host,
#     'database': database,
#     'port': port
# }
class MySqlOperator:

    def __init__(self):
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=database)

    def searchbysql(self, sql):
        global cursor
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            self.conn.close()

    def operatebysql(self, sql, val):
        global cursor
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            return self.conn.commit()
        finally:
            cursor.close()
            self.conn.close()
