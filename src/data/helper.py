import logging
from typing import Dict, Optional, Any, List
import pandas as pd
from sqlalchemy import text

from src.database.connection import DBConnection


class Helper:
    def __init__(self):
        self._db_manager = DBConnection()
        
    def get_user_products(self, user_id: int) -> List[Dict[str, Any]]:
        query = """
        SELECT p.* FROM products p
        INNER JOIN user_products up ON p.id = up.product_id
        WHERE up.user_id = :user_id;
        """
        params = {"user_id": user_id}
        db_connection = self._db_manager.connect()
        try:
            product_df: pd.DataFrame = pd.read_sql(
                sql=text(query),
                con=db_connection,
                params=params
            )
            product_list: List[Dict[str, Any]] = product_df.to_dict(orient="records")
            return product_list  # Returns all products, not just the first one
        except mysql.connector.Error as e:
            logging.info(f"Error getting user products: {e}")
            return []
        finally:
            self._db_manager.close(db_connection)    
    
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

    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT * FROM products
            WHERE id = :product_id;
        """
        params = {"product_id": product_id}
        db_connection = self._db_manager.connect()
        try:
            product_df: pd.DataFrame = pd.read_sql(
                sql=text(query),
                con=db_connection,
                params=params
            )
            if not product_df.empty:
                product_data = product_df.to_dict(orient="records")[0]
            else:
                product_data = None

        except Exception as e:
            logging.error(f"Error getting product: {e}")
            product_data = None

        finally:
            self._db_manager.close(db_connection)

        return product_data

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