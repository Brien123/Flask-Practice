import logging
from typing import Dict, Optional, Any, List
import pandas as pd
from sqlalchemy import text

from src.database.connection import DBConnection


class Helper:
    def __init__(self):
        self._db_manager = DBConnection()

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