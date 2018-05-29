import json
import psycopg2
import dataset
from sqlalchemy.sql import select

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


def insert_finding_results(id, request_params, status, created_date, updated_date):
    # TODO wydzielić poniższe rzeczy do metody i jej użyć tutaj oraz w shop_collection_extractor (zwrócić parę database_url, schema)
    database_url = 'postgresql://' + db_config['username'] + ":" + db_config['password'] + "@" + db_config[
        'host'] + "/" + db_config['db_name']
    schema = db_config['schema']

    with dataset.connect(database_url, schema) as database:
        finding_results_table = database['finding_results']
        data = dict(id=id, request_params=request_params, status=status, result="", created_date=created_date,
                    updated_date=updated_date)
        finding_results_table.insert(data)


def get_processing_element_status(id):
    # TODO wydzielić poniższe rzeczy do metody i jej użyć tutaj oraz w shop_collection_extractor (zwrócić parę database_url, schema)
    database_url = 'postgresql://' + db_config['username'] + ":" + db_config['password'] + "@" + db_config[
        'host'] + "/" + db_config['db_name']
    schema = db_config['schema']

    id = id.replace("/", "")

    with dataset.connect(database_url, schema) as database:
        arr = []
        stmt = database.query("SELECT * FROM pite.finding_results WHERE id='" + id + "'")
        for row in stmt:
            arr.append(row)

    if len(arr) == 0:
        return False
    else:
        return str(arr[0]['status'])
