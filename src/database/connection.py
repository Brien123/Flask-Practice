from mysql.connector.pooling import MySQLConnectionPool
from src.config import Config
from mysql.connector import Error
import logging


class DBConnection:
    def __init__(self):
        self.config = Config()
        self._pool = self._create_pool()

    def _create_pool(self):
        try:
            port = int(self.config.DB_PORT)
            pool = MySQLConnectionPool(
                pool_name=self.config.POOL_NAME,
                pool_size=self.config.POOL_SIZE,
                host=self.config.DB_HOST,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                port=port
            )
            logging.info(f"INFO: Connection Pool '{self.config.POOL_NAME}' initialized with size {self.config.POOL_SIZE}.")
            return pool
        except Error as e:
            logging.info(f"ERROR: Failed to create MySQL connection pool: {e}")
            return None

    def connect(self):
        if self._pool:
            try:
                return self._pool.get_connection()
            except Error as e:
                print(f"ERROR: Failed to borrow connection from pool: {e}")
                return None
        return None

    def close(self, connection):
        if connection:
            connection.close()

    def shutdown_pool(self):
        if self._pool:
            self._pool = None