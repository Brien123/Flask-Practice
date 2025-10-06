import logging
from typing import Dict, Optional, Any, List
import pandas as pd
from sqlalchemy import text
import mysql.connector

from src.database.connection import DBConnection


class Helper:
    def __init__(self):
        self._db_manager = DBConnection()

    def get_products_by_category(self, category_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT * FROM products
            WHERE category_id = :category_id;
        """
        params = {"category_id": product_id}
        db_connection = self._db_manager.connect()
        try:
            product_df: pd.DataFrame = pd.read_sql(
                sql=text(query),
                con=db_connection,
                params=params
            )
            product_list: List[Dict[str, Any]] = product_df.to_dict(orient="records")
            product_data = product_list[0]

        except mysql.connector.Error as e:
            logging.info(f"Error getting products by category: str{e}")
            product_data = None

        finally:
            self._db_manager.close(db_connection)

        return product_data