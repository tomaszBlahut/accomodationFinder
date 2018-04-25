import json
import psycopg2

with open('config/config.json') as json_data:
    config = json.load(json_data)
    
dbconfig = config["database"]

def execute(query):
    conn = None
    try:
        conn = psycopg2.connect(host=dbconfig["host"], database=dbconfig["dbname"],
                                user=dbconfig["username"], password=dbconfig["password"])
        cur = conn.cursor()
        cur.execute(query)
        records = cur.fetchall()
        cur.close()
        return records
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()