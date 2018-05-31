from flask_api import FlaskAPI
from flask_cors import CORS
from flask import request
from flask import Response
import sys
import uuid
import datetime
import json
from threading import Thread

sys.path.append(".")
import shop_collection_extractor
import db

app = FlaskAPI(__name__)
CORS(app)


@app.route('/example/', methods=['GET'])
def example():
    return {'Hello, ': 'world!'}


@app.route('/shop/', methods=['GET'])
def get_shops():
    center_latitude = float(request.args.get('latitude'))
    center_longitude = float(request.args.get('longitude'))
    radius = float(request.args.get('radius'))

    return shop_collection_extractor.get_shop_collection_within_range(center_longitude, center_latitude, radius)


def start_new_searching(result_id, json_request, status_value):
    current_datetime = datetime.datetime.now()

    db.insert_finding_results(result_id, json_request, status_value, current_datetime, current_datetime)

    # TODO rozpoczęcie wyszukiwania w nowym wątku
    # thread = Thread(target=__funkcja_wyszukująca__)
    # thread.start()


@app.route('/search/', methods=['POST'])
def start_searching():
    result_id = str(uuid.uuid4())
    json_request = request.get_json()

    # TODO zmienić 0 na enuma
    start_new_searching(result_id, str(json_request), 0)

    return result_id


@app.route('/rerun-search/', methods=['GET'])
def rerun_searching():
    result_id = request.args.get('id')

    request_params = db.get_processing_element_request_params(result_id)

    if not request_params:
        return Response(status=412)

    new_result_id = str(uuid.uuid4())

    # TODO zmienić 1 na enuma
    start_new_searching(new_result_id, request_params, 1)

    return new_result_id
