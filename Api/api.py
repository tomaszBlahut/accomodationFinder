from flask_api import FlaskAPI
from flask_cors import CORS
from flask import request
from flask import Response
import json
import uuid
from threading import Thread
from implementation.shop_dal import get_shop_collection_within_range, get_shop_names_within_area_bounds, get_all_shop_types
from implementation.search_results_dal import insert_finding_results, get_processing_element_request_params, get_search_results
from implementation.models.search_state import SearchState
from implementation.search_processor.search_processor import SearchProcessor
from implementation.encoders.datetime_encoder import DateTimeEncoder

app = FlaskAPI(__name__)
CORS(app)

json_mimetype = 'application/json'


@app.route('/shop/<float:center_latitude>/<float:center_longitude>/<float:radius>', methods=['GET'])
def get_shops(center_latitude, center_longitude, radius):
    shops = get_shop_collection_within_range(center_longitude,
                                             center_latitude,
                                             radius)

    response = {"shops": shops}

    return Response(json.dumps(response), 200, mimetype=json_mimetype)


@app.route('/shopTypes', methods=['POST'])
def get_shops_types_by_area():
    area_bounds = request.get_json()
    shops = get_shop_names_within_area_bounds(area_bounds)

    response = {"shops": shops}

    return Response(json.dumps(response), 200, mimetype=json_mimetype)


@app.route('/shopTypes', methods=['GET'])
def get_all_shops_types():
    shops = get_all_shop_types()

    response = {"shops": shops}

    return Response(json.dumps(response), 200, mimetype=json_mimetype)


def start_new_searching(result_id, json_request, status_value):
    insert_finding_results(result_id, json_request, status_value)

    thread = Thread(target=SearchProcessor.process_search,
                    args=(result_id, json_request))
    thread.start()


@app.route('/search', methods=['POST'])
def start_searching():
    result_id = str(uuid.uuid4())
    json_request = request.get_json()

    start_new_searching(result_id, json.dumps(json_request), SearchState.NEW)    

    response = json.dumps({"id": result_id})
    return Response(response, 200, mimetype=json_mimetype)


@app.route('/rerun-search/<result_id>', methods=['GET'])
def rerun_searching(result_id):
    request_params = get_processing_element_request_params(result_id)

    if not request_params:
        return Response(status=412)

    new_result_id = str(uuid.uuid4())

    start_new_searching(new_result_id, request_params, SearchState.NEW)

    response = json.dumps({"id": new_result_id})
    return Response(response, 200, mimetype=json_mimetype)


@app.route('/result/<id>', methods=['GET'])
def get_results(id):
    results = get_search_results(id)

    return Response(json.dumps(results, cls=DateTimeEncoder), 200, mimetype=json_mimetype)
