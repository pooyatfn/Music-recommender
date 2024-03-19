import psycopg2

from db.configs import *

conn = psycopg2.connect(POSTGRESQL_URL)
cur = conn.cursor()
cur.execute("""
    Drop table Request
""")
data = cur.fetchall()
print(data)
conn.commit()
cur.close()
conn.close()
