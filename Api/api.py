from flask_api import FlaskAPI
from flask_cors import CORS
from flask import request
import sys

sys.path.append(".")
import shop_collection_extractor

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
