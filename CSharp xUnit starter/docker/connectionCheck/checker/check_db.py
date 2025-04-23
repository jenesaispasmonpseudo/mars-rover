import os
import time
import psycopg2

host = os.getenv("DB_HOST", "db")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "mypassword")
dbname = os.getenv("DB_NAME", "postgres")

while True:
    try:
        conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
        print("Connexion réussie !")
        conn.close()
        break
    except Exception as e:
        print("Connexion échouée")
        print(str(e))
        time.sleep(5)
