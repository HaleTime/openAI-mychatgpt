from mysql.connector import pooling
import configparser
import logging

logger = logging.getLogger("connector")


class ConnectorPool:
    pool = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../dbconfig.ini')

        # 获取配置文件中的值
        database = 'xiaobaimao'
        host = config.get(database, 'host')
        port = config.getint(database, 'port')
        user = config.get(database, 'username')
        password = config.get(database, 'password')

        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database,
            'port': port
        }

        try:
            self.pool = pooling.MySQLConnectionPool(pool_name='mypool',
                                                    pool_size=10,
                                                    **config)
        except Exception as e:
            logger.error("Create pool error! ", e)

    def get_connection(self):
        if self.pool is not None:
            connection = self.pool.get_connection()
            return connection
        else:
            raise Exception('Connector\'s pool is None')
