from src.database.connection import DBConnection
from src.data.helper import Helper

helper = Helper()

products = helper.get_user_products(user_id=26)
print(products)
