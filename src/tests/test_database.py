from src.database.connection import DBConnection
from src.data.helper import Helper

helper = Helper()

products = helper.get_products()
print(products)
