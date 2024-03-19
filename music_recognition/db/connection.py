import psycopg2
from sqlalchemy.testing.exclusions import closed

from utils.logger import Logger

logger = Logger("db.connection.log")


class Connection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None

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
                updated_data = cursor.fetchall()
                logger.info(f"Updated data: {updated_data}")
                return updated_data
            except psycopg2.DatabaseError as e:
                logger.error(f"Query failed: {e}")
                self.conn.rollback()
                return None
