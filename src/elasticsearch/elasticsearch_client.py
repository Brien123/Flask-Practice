import logging
from src.config import Config
from elasticsearch import Elasticsearch


class ElasticSearchClient:
    def __init__(self):
        self.config = Config()
        self.elastic_url = self.config.ELASTICSEARCH_URL
        self.client = None

    def connect(self):
        if self.client is None:
            try:
                self.client = Elasticsearch([self.elastic_url], basic_auth=(self.config.ELASTIC_USER, self.config.ELASTIC_PASSWORD),
                    verify_certs=False, request_timeout=30)
                if self.client.ping():
                    logging.info("Successfully connected to Elasticsearch")
                else:
                    logging.error("Failed to ping Elasticsearch")
                    self.client = None
            except Exception as e:
                logging.error(f"Failed to connect to Elasticsearch: {e}")
                self.client = None
        return self.client

    def create_index(self, index_name: str, mapping: dict):
        client = self.connect()
        if client:
            try:
                if client.indices.exists(index=index_name):
                    logging.info(f"Index {index_name} already exists")
                    return True

                client.indices.create(index=index_name, body=mapping)
                logging.info(f"Index {index_name} created successfully")
                return True
            except Exception as e:
                logging.error(f"Failed to create index {index_name}: {e}")
                return False
        return False

    def delete_index(self, index_name: str):
        client = self.connect()
        if client:
            try:
                if not client.indices.exists(index=index_name):
                    logging.info(f"Index {index_name} does not exist")
                    return True

                client.indices.delete(index=index_name)
                logging.info(f"Index {index_name} deleted successfully")
                return True
            except Exception as e:
                logging.error(f"Failed to delete index {index_name}: {e}")
                return False
        return False

    def index_exists(self, index_name: str) -> bool:
        client = self.connect()
        if client:
            try:
                return client.indices.exists(index=index_name)
            except Exception as e:
                logging.error(f"Failed to check if index {index_name} exists: {e}")
                return False
        return False