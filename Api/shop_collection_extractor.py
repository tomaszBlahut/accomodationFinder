from haversine_formula.haversine_formula import HaversineFormula
import dataset
import json


def get_shop_collection_within_range(center_longitude, center_latitude, radius):
    with open('config/config.json') as json_data:
        config = json.load(json_data)
    db_config = config["database"]

    square_limitations = HaversineFormula.calculate_square_limitations(center_longitude, center_latitude, radius)

    max_latitude = square_limitations[0]
    min_latitude = square_limitations[1]
    max_longitude = square_limitations[2]
    min_longitude = square_limitations[3]

    database_url = 'postgresql://' + db_config['username'] + ":" + db_config['password'] + "@" + db_config[
        'host'] + "/" + db_config['db_name']
    schema = db_config['schema']

    shops = []
    with dataset.connect(database_url, schema) as database:
        for shop in database['shop']:
            shop_latitude = shop['latitude']
            shop_longitude = shop['longitude']
            if min_longitude <= shop_longitude <= max_longitude and min_latitude <= shop_latitude <= max_latitude:
                shops.append(shop)

    return shops
