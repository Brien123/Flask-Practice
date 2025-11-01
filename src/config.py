import os
import os.path
from dotenv import load_dotenv



#dotenv_path = load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__)))



load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'a-secret-key'

    # Database configuration
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 3306)
    DB_NAME = os.getenv("DB_NAME")
    POOL_NAME = 'flask_pool'
    POOL_SIZE = 5

    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis configuration
    REDIS_URL = os.getenv('REDIS_BROKER_URL')

    # Elasticsearch configuration
    ELASTIC_USER = os.getenv('ELASTIC_USER')
    ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
    ELASTICSEARCH_URL = "https://127.0.0.1:9200"

    FLASK_APP = 'wsgi.py'
    FLASK_ENV = os.environ.get('ENV')