import json
import psycopg2

with open('config/config.json') as json_data:
    config = json.load(json_data)

db_config = config["database"]


def execute(query):
    conn = None
    try:
        conn = psycopg2.connect(host=db_config["host"], database=db_config["db_name"],
                                user=db_config["username"], password=db_config["password"])
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
