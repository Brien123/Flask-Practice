import logging
import math
from typing import List, Dict, Any

from elasticsearch.helpers import bulk

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

    def create_index(self, index_name: str, mapping: dict) -> bool:
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

    def delete_index(self, index_name: str) -> bool:
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

    def bulk_index_products_data(self, products_data: List[Dict[str, Any]], index_name: str = "products") -> bool:

        MAPPED_FIELDS = {
            "id", "user_id", "category_id", "brand_id", "country", "price", "whole_sale",
            "name", "name_fr", "currency", "description", "description_fr", "search_index",
            "hash", "image", "image_original", "image_thumb", "image_medium",
            "created_at", "updated_at", "deleted_at", "latitude", "longitude", "location"
        }

        NUMERICAL_FIELDS = {"price", "whole_sale", "latitude", "longitude", "id", "user_id"}
        DATE_FIELDS = {"created_at", "updated_at", "deleted_at"}

        client = self.connect()
        if client:
            try:
                actions = []

                for product in products_data:
                    for key, value in product.items():
                        if value is None:
                            continue
                        if isinstance(value, float) and math.isnan(value):
                            product[key] = None
                        elif isinstance(value, str) and value.strip().lower() in ['nan', 'null', 'none', '']:
                            product[key] = None

                for product in products_data:
                    doc_source = {}
                    product_id = None

                    for field in MAPPED_FIELDS:
                        value = product.get(field)
                        final_value = value

                        if field in DATE_FIELDS:
                            if value is None:
                                final_value = None
                            elif isinstance(value, str):
                                if value.strip() == '':
                                    final_value = None
                                else:
                                    if 'T' in value:
                                        final_value = value
                                    else:
                                        final_value = value
                            elif isinstance(value, (int, float)):
                                try:
                                    from datetime import datetime
                                    final_value = datetime.fromtimestamp(value / 1000).isoformat()
                                except (ValueError, OSError, TypeError):
                                    final_value = None
                            else:
                                final_value = None

                        elif field in NUMERICAL_FIELDS:
                            if value is None:
                                final_value = None
                            elif isinstance(value, str) and value.strip() == '':
                                final_value = None
                            elif (isinstance(value, str) and value.lower() in ['nan', 'null', 'none']):
                                final_value = None
                            elif isinstance(value, float) and math.isnan(value):
                                final_value = None
                            else:
                                try:
                                    if isinstance(value, str) and value.strip().lower() == 'nan':
                                        final_value = None
                                    elif field in ["price", "latitude", "longitude"]:
                                        float_val = float(value)
                                        if math.isnan(float_val):
                                            final_value = None
                                        else:
                                            final_value = float_val
                                    elif field in ["whole_sale", "id", "user_id"]:
                                        float_val = float(value)
                                        if math.isnan(float_val):
                                            final_value = None
                                        else:
                                            final_value = int(float_val)
                                except (TypeError, ValueError, OverflowError):
                                    final_value = None

                        else:
                            if value is None:
                                final_value = None
                            elif isinstance(value, float) and math.isnan(value):
                                final_value = None
                            elif isinstance(value, str) and value.strip().lower() in ['nan', 'null', 'none']:
                                final_value = None
                            else:
                                final_value = value

                        if field == "id":
                            product_id = final_value

                        doc_source[field] = final_value

                    if product_id is None:
                        continue

                    if isinstance(product_id, float) and math.isnan(product_id):
                        continue

                    action = {
                        "_index": index_name,
                        "_id": product_id,
                        "_source": doc_source
                    }
                    actions.append(action)

                if not actions:
                    return True

                successes, errors = bulk(
                    client,
                    actions,
                    raise_on_error=False
                )

                if errors:
                    for error in errors[:5]:
                        pass

                return len(actions) == successes

            except Exception as e:
                return False

    def search(self, search_term: str, index_name: str = "products", size: int = 10, page: int = 1) -> List[Dict[str, Any]]:
        client = self.connect()
        if client:
            try:
                offset = int((page - 1) * size)
                query = {
                    "min_score": 1,
                    "size": size,
                    "from": offset,
                    "query": {
                        "multi_match": {
                            "query": search_term,
                            "fields": [
                                "name^2",
                                "name_fr^2",
                                "hash",
                                "description",
                                "description_fr",
                                "search_index",
                            ],
                            "fuzziness": "AUTO",
                            "type": "best_fields"
                        }
                    }
                }
                response = client.search(
                    index=index_name,
                    body=query
                )
                return [hit['_source'] for hit in response['hits']['hits']]
            except Exception as e:
                print(f"Error during search: {e}")
                return []
        return []