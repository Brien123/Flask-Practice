import mysql.connector

from config import Config

import logging

class DBConnection:
    def __init__(self):
        self.connection = None

    # TODO: create a method to connect to the database using the database credentials from config class
    def connect(self):
        try:
            self.connection = mysql.connector.connect(

                host=Config.DB_HOST,

                port=Config.DB_PORT,

                password=Config.DB_PASSWORD,

                user=Config.DB_USER,

                dbname=Config.DB_NAME



            )

        except Exception as e:

            logging.info(f"An error uccord during database connection: str({e})")

