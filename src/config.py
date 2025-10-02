import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key'

    # Database configuration
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT', 3306)
    DB_NAME = os.environ.get('DB_NAME')
    POOL_NAME = 'njanggi_pool'
    POOL_SIZE = 5

    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_BROKER_URL')

    # Elasticsearch configuration
    ELASTIC_USER = os.environ.get('ELASTIC_USER')
    ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')
    ELASTICSEARCH_URL = f"http://{ELASTIC_USER}:{ELASTIC_PASSWORD}@localhost:9200"

    FLASK_APP = 'wsgi.py'
    FLASK_ENV = os.environ.get('ENV')