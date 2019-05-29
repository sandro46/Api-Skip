"""Test PostgreSQL connection."""
import psycopg2

connection_parameters = {
    'host': "192.168.101.13",
    'database': 'app',
    'user': 'web',
    'password': 'webpass'
}
conn = psycopg2.connect(**connection_parameters)
print(conn)
cur = conn.cursor()
cur.execute("select current_date date")
res = cur.fetchone()
print(res)