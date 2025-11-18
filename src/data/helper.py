import logging
from typing import Dict, Optional, Any, List
import pandas as pd
from sqlalchemy import text, bindparam

from src.database.connection import DBConnection


class Helper:
    def __init__(self):
        self._db_manager = DBConnection()

    def get_product(self, product_id: int, ) -> Optional[Dict[str, Any]]:
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
     
    def get_product_by_category(self, category_id: int, size: int=5, page: int = 1) -> Optional[List[Dict[str, Any]]]:
        offset = (page - 1) * size
        query = """
            SELECT * FROM products
            WHERE category_id = category_id
            ORDER BY created_at
            LIMIT :size
            OFFSET :offset;
        """
        params = {"size":size, "offset":offset, "category_id": category_id}
        db_connection = self._db_manager.connect()
        try:
            products_df: pd.DataFrame = pd.read_sql(text(query), con=db_connection, params=params)
            products_list = products_df.to_dict(orient="records")
        except Exception as e:
            logging.error(f"Error getting products by category: {e}")
            products_list = None
        finally:
            self._db_manager.close(db_connection)

        return products_list

    def get_product_by_user(self,  user_id: int, size: int = 5, page: int = 1)-> Optional[List[str: Any]]:
        offset = (page - 1) * size
        query = """
            SELECT * FROM products
            WHERE user_id = user_id
            ORDER BY created_at
            LIMIT :size
            OFFSET :offset;
        """
        params = {"size":size, "user_id":user_id, "offset":offset}
        db_connection = self._db_manager.connect()
        try:
            products_df: pd.DataFrame = pd.read_sql(text(query), con=db_connection, params=params)
            product_list = products_df.to_dict(orient="records")
        except Exception as e:
            logging.error(f"Error getting products for user: {e}")
            product_list = None
        finally:
            self._db_manager.close(db_connection)

        return product_list

    def get_products_from_list(self, product_ids: List[int]):
        if not product_ids:
            return []

        query = text("""
            SELECT * FROM products
            WHERE id IN :product_ids
        """).bindparams(bindparam("product_ids", expanding=True))

        db_connection = self._db_manager.connect()
        try:
            result = db_connection.execute(query, {"product_ids": product_ids})
            products_df = pd.DataFrame(result.fetchall(), columns=result.keys())
            product_list = products_df.to_dict(orient="records")
        except Exception as e:
            logging.error(f"Error getting products from list: {e}")
            product_list = []
        finally:
            self._db_manager.close(db_connection)

        return product_list

    def fetch_products(self, page: int = 1, size: int = 20):
        offset = (page - 1) * size
        query = """
            SELECT * from products
            ORDER BY created_at
            LIMIT :size  
            OFFSET :offset
        """
        params = {"size": size, "offset": offset}
        db_connection = self._db_manager.connect()
        try:
            products_df: pd.DataFrame = pd.read_sql(text(query), con=db_connection, params=params)
            product_list = products_df.to_dict(orient="records")
        except Exception as e:
            logging.error(f"Error getting products for user: {e}")
            product_list = None
        finally:
            self._db_manager.close(db_connection)

        return product_list