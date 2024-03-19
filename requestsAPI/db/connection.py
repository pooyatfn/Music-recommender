import psycopg2
from sqlalchemy.testing.exclusions import closed

from db.queries import *
from utils.logger import Logger

logger = Logger("db.connection.log")


class Connection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None
        if self.open():
            self.execute_query(CREATE_REQUEST_TABLE_IN_DBAAS)
            self.close()

    def open(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
        except psycopg2.DatabaseError as e:
            logger.error(f"Database connection failed: {e}")
            return False
        return True

    def close(self):
        if self.conn is not closed:
            self.conn.close()

    def execute_query(self, query, params=None):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, params or ())
                self.conn.commit()
                if query is INSERT_DATA_INTO_REQUEST_TABLE:
                    inserted_data = cursor.fetchall()
                    logger.info(f"Inserted data: {inserted_data}")
                    return inserted_data
            except psycopg2.DatabaseError as e:
                logger.error(f"Query failed: {e}")
                self.conn.rollback()
                return None
