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


def get_database_connection_params():
    database_url = 'postgresql://' + db_config['username'] + ":" + db_config['password'] + "@" + db_config[
        'host'] + "/" + db_config['db_name']
    schema = db_config['schema']
    return database_url, schema


def insert_finding_results(id, request_params, status, created_date, updated_date):
    with dataset.connect(*get_database_connection_params()) as database:
        finding_results_table = database['finding_results']
        data = dict(id=id, request_params=request_params, status=status, result="", created_date=created_date,
                    updated_date=updated_date)
        finding_results_table.insert(data)


def get_processing_element_request_params(id):
    id = id.replace("/", "")

    with dataset.connect(*get_database_connection_params()) as database:
        row_from_id = dataset.Table(database, 'finding_results').find_one(id=id)
    return row_from_id['request_params']
