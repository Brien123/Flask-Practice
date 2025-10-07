from src.elasticsearch.mapping import products_mapping

from src.elasticsearch.elasticsearch_client import ElasticSearchClient

es = ElasticSearchClient()
print(es.create_index("products", products_mapping))