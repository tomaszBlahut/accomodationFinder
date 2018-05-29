from flask_api import FlaskAPI
from flask_cors import CORS
from flask import request
import sys
import uuid
import datetime
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


@app.route('/search/', methods=['POST'])
def start_searching():
    id = uuid.uuid4()
    json_request = request.get_json()
    radius = float(json_request['radius'])
    start = json_request['start']
    wages = json_request['wages']
    mesh_density = float(json_request['mesh_density'])

    current_datetime = datetime.datetime.now()

    # TODO zmienić stringa NEW na enuma
    db.insert_finding_results(id, str(json_request), "NEW", current_datetime, current_datetime)

    # TODO rozpoczęcie wyszukiwania w nowym wątku
    # thread = Thread(target=__funkcja_wyszukująca__)
    # thread.start()

    return id
