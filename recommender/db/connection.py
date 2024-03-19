import psycopg2
import select
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
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

    def db_listen(self):
        cur = self.conn.cursor()
        cur.execute("LISTEN status_changed;")

        while True:
            select.select([self.conn], [], [])
            self.conn.poll()
            while self.conn.notifies:
                notification = self.conn.notifies.pop()
                print(f"Received notification on channel '{notification.channel}': {notification.payload}")

    def set_isolation_level(self):
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

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
