import dataset
import datetime
import json
from .db import get_database_connection_params
from .numpy_encoder import NumpyEncoder


def insert_finding_results(result_id, request_params, status):
    current_datetime = datetime.datetime.now()

    with dataset.connect(*get_database_connection_params()) as database:
        finding_results_table = database['finding_results']
        data = dict(id=result_id,
                    request_params=request_params,
                    status=int(status),
                    result="",
                    created_date=current_datetime,
                    updated_date=current_datetime)

        finding_results_table.insert(data)


def get_processing_element_request_params(result_id):
    result_id = result_id.replace("/", "")

    with dataset.connect(*get_database_connection_params()) as database:
        row_from_id = dataset.Table(database, 'finding_results').find_one(id=result_id)
    return row_from_id['request_params']


def get_search_results(result_id):
    with dataset.connect(*get_database_connection_params()) as database:
        results = dataset.Table(database, 'finding_results').find_one(id=result_id)
    return results


def update_search_result_status(result_id, status):
    current_datetime = datetime.datetime.now()

    with dataset.connect(*get_database_connection_params()) as database:
        table = database['finding_results']        
        table.update(dict(id=result_id,
                          status=int(status),
                          updated_date=current_datetime), ['id'])


def update_search_result_output(result_id, result):
    current_datetime = datetime.datetime.now()

    with dataset.connect(*get_database_connection_params()) as database:
        table = database['finding_results']
        table.update(dict(id=result_id,
                          result=json.dumps(result, cls=NumpyEncoder),
                          updated_date=current_datetime), ['id'])
