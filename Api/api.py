import sys
sys.path.append("./haversine_formula")
from haversine_formula import HaversineFormula
from flask_api import FlaskAPI
from flask_cors import CORS
from flask import request
import dataset
import json

app = FlaskAPI(__name__)
CORS(app)

with open('config/config.json') as json_data:
    config = json.load(json_data)
db_config = config["database"]


@app.route('/example/', methods=['GET'])
def example():
    return {'Hello, ': 'world!'}


@app.route('/shop/', methods=['GET'])
def get_shops():
    center_latitude = float(request.args.get('latitude'))
    center_longitude = float(request.args.get('longitude'))
    radius = float(request.args.get('radius'))

    coordinates = HaversineFormula.calculate_square_bounds(center_longitude, center_latitude, radius)

    max_latitude = coordinates['up']['latitude']
    min_latitude = coordinates['down']['latitude']
    max_longitude = coordinates['right']['longitude']
    min_longitude = coordinates['left']['longitude']

    database_url = 'postgresql://' + db_config['username'] + ":" + db_config['password'] + "@" + db_config[
        'host'] + "/" + db_config['db_name']
    schema = 'pite'

    shops = []
    with dataset.connect(database_url, schema) as database:
        for shop in database['shop']:
            shop_lalitude = shop['latitude']
            shop_longitude = shop['longitude']
            if min_longitude <= shop_longitude <= max_longitude and min_latitude <= shop_lalitude <= max_latitude:
                shops.append(shop)

    return shops
