import time
import psycopg2
from psycopg2 import OperationalError
import os

def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host="postgres",
                port="5432"
            )
            conn.close()
            print("PostgreSQL is ready!")
            break
        except OperationalError:
            print("PostgreSQL not ready, retrying...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_postgres()
