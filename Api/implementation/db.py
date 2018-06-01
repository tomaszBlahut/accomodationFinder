import json
import dataset

with open('implementation/config/config.json') as json_data:
    config = json.load(json_data)

db_config = config["database"]


def get_database_connection_params():
    database_url = 'postgresql://%(username):%(password)@%(host)/%(db_name)' % {'username': db_config['username'],
                                                                                'password': db_config['password'],
                                                                                'host': db_config['host'],
                                                                                'db_name': db_config['db_name']}
    schema = db_config['schema']
    return database_url, schema


def insert_finding_results(result_id, request_params, status, created_date, updated_date):
    with dataset.connect(*get_database_connection_params()) as database:
        finding_results_table = database['finding_results']
        data = dict(id=result_id, request_params=request_params, status=status, result="", created_date=created_date,
                    updated_date=updated_date)
        finding_results_table.insert(data)


def get_processing_element_request_params(result_id):
    result_id = result_id.replace("/", "")

    with dataset.connect(*get_database_connection_params()) as database:
        row_from_id = dataset.Table(database, 'finding_results').find_one(id=result_id)
    return row_from_id['request_params']
