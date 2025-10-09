import logging
from typing import List, Dict, Optional, Any
import pandas as pd
from sqlalchemy import text

from src.database.connection import DBConnection


class Helper:
    def __init__(self):
        self._db_manager = DBConnection()
        
    
    def get_products_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT * FROM products
            WHERE category_id = :category_id;
        """
        params = {"category_id": category_id}
        db_connection = self._db_manager.connect()
        try:
            product_df: pd.DataFrame = pd.read_sql(
                sql=text(query),
                con=db_connection,
                params=params
            )
            product_list: List[Dict[str, Any]] = product_df.to_dict(orient="records")
        except mysql.connector.Error as e:
            logging.info(f"Error getting products by category: {e}")
            product_list = []
        finally:
            self._db_manager.close(db_connection)
        
        return product_list    

    class DatabaseManager:
        def __init__(self):
            pass
    
    class ProductService:
        def __init__(self, db_manager):
            """
            Initializing ProductService, with a database manager.
                
            Args:
                db_manager: The database manager that provides connection context
            """
            self._db_manager = db_manager
    
    # Usage now
    db_manager = DatabaseManager()
    product_service = ProductService(db_manager)        
                
    def get_user_products(self, user_id: int) -> List[Dict[str, Any]]:
        """    
        Retrieves now all products for a specific user, from the database.
                
        Args: 
            user_id: The ID of the user, whose products we're to retrieve
                    
        Returns:
            List of dictionaries containing product data, or an empty list if "error" occurs    
        """
            # Let's start now with the SQL query, of placeholder :user_id
        QUERY_USER_PRODUCTS = """
            SELECT * FROM products
            WHERE user_id = :user_id;
        """
            
        params = {"user_id": user_id}
            
        try:
            # Using the 'with' statement for the connection management(Context Manager)
            # This is what will help to automatically close the connection.
            with self._db_manager.connect() as db_connection:
                # I'm using 'pandas.read_sql', with the parametrized query
                product_df: pd.DataFrame = pd.read_sql(
                    sql = text(QUERY_USER_PRODUCTS),
                    con = db_connection,
                    params = params
                )
                # Now let's convert the above DataFrame, into a list of dictionaries(records)
                product_list: List[Dict[str, Any]] = product_df.to_dict(orient="records")
                return product_list
                
        except Exception as e:
            # Catching and logging any errors that may arise(e.g DB Connection error, SQL error, etc.)
            logging.error(f"Sorry! Failed to retrieve products for user {user_id}: {e}")
            return []
                  
    

    def get_products(self) -> Optional[List[Dict[str, Any]]]:
        query = "SELECT * FROM products"
        db_connection = self._db_manager.connect()
        try:
            products_df: pd.DataFrame = pd.read_sql(text(query), con=db_connection)
            products_list = products_df.to_dict(orient="records")
        except Exception as e:
            logging.error(f"Error getting products: {e}")
            products_list = None
        finally:
            self._db_manager.close(db_connection)

        return products_list