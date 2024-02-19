import mysql.connector.pooling
from config.config import db_config


class DBConnector:
    _pool = None

    def __init__(self):
        if not DBConnector._pool:
            self._create_pool()

    def _create_pool(self):
        DBConnector._pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="my_pool",
            pool_size=5,  # Adjust the pool size as needed
            **db_config
        )

    def __enter__(self):
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()

    def get_connection(self):
        return DBConnector._pool.get_connection()

    def start_transaction(self):
        self.connection.start_transaction()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"SQL Error: {err}")
            raise

    def execute_many_query(self, query, values=None):
        try:
            self.cursor.executemany(query, values)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"SQL Error: {err}")
            raise
