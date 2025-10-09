import logging
from typing import Dict, Optional, Any, List
import pandas as pd
from sqlalchemy import text
from src.database.connection import DBConnection



class Helper:
    def __init__(self):
        self._db_manager = DBConnection()

    def get_product(self, product_id, int) -> Optional[Dict[str, Any]]:
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
    

    def get_products(self, int) -> Optional[List[Dict[str, Any]]]:
        query = "SELECT * FROM products"
        db_connection = self._db_manager.connect()
        try:
            products_df: pd.DataFrame = pd.read_sql(text(query))
            products_list = products_df.to_dict(orient="records")
        except Exception as e:
            logging.error(f"Error getting products: {e}")
            products_list = None
        finally:
            self._db_manager.close(db_connection)

        return products_list
    



    def get_product_id(self, user_id: int) -> Optional[Dict[str, Any]]:

        query = "SELECT * FROM product  WHERE  user_id = :user_id "

        params = {"user_id":user_id}

        db_engine = self._db_manager.get_engine()

        try:
            product_df: pd.DataFrame = pd.read_sql(

                text(query),

                con=db_engine,

                params=params
            )
            if not product_df.empty:

                product_list = product_df.to_dict(orient="records")

                return product_list

            else:

                return []

        except Exception as e:

            logging.error(f"Error getting product: {e}")

            return []
        




    def  get_product_category(self, caterory_id: int) -> list[Dict[str, Any]]:

        query = "SELECT * FROM product WHERE category_id = category_id"

        params = {"category_id":caterory_id}

        db_ingine = self._db_manager.get_engine()

        try:

            product_df: pd.DataFrame = pd.read_sql(text(query), con=db_ingine, params=params)

            if not product_df.empty:

                product_list = product_df.to_dict(orient="records")

                return product_list
            
            else:

                return []
            
        except Exception as e:

            logging.error(f"Error can not get product py category: {e}")

            return []





    def get_product_date(self, created_at: int) -> List[Dict[str, Any]]:

        query = "SELECT * FROM products WHERE created_at = created_at"

        params = {"created_at": created_at}

        db_engine = self._db_manager.get_engine()

        try:
                product_df: pd.DataFrame = pd.read_sql(sql=query, con=db_engine, params=params)

                if not product_df.empty:

                    product_list = product_df.to_dict(orient="records")

                    return product_list

                else:

                    return []

        except Exception as e:
                
            logging.error(f"Error to get products by date: {e}")


            return []

        











     



   