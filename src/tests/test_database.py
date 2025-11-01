from src.data.helper import Helper


 

#  instance of my DBConnection 
db_manager = DBConnection()

# An instance of Helper to pass the db_manager to it
helper = Helper(db_manager)

#  Call the method 
products = helper.get_product_category(4)

print(products)




