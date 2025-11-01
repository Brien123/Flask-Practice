from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from src.config import Config
import logging
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env.example'))

class DBConnection:
    def __init__(self):
        self.config = Config()
        self._engine = self._create_engine()

    def _create_engine(self):
        try:
            engine = create_engine(
                self.config.SQLALCHEMY_DATABASE_URI,
                poolclass=QueuePool,
                pool_size=self.config.POOL_SIZE,
                max_overflow=10,
                pool_pre_ping=True
            )
            logging.info(f"SQLAlchemy engine created with pool size {self.config.POOL_SIZE}")
            return engine
        except Exception as e:
            logging.error(f"ERROR: Failed to create SQLAlchemy engine: {e}")
            return None

    def connect(self):
        if self._engine:
            try:
                return self._engine.connect()
            except Exception as e:
                logging.error(f"ERROR: Failed to get connection from engine: {e}")
                return None
        return None

    def close(self, connection):
        if connection:
            connection.close()

    def get_engine(self):
        return self._engine

    def shutdown_pool(self):
        if self._engine:
            self._engine.dispose()