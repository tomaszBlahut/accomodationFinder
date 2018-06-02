from .haversine_formula.haversine_formula import HaversineFormula
import dataset
import json
from .db import get_database_connection_params


def get_shop_collection_within_range(center_longitude, center_latitude, radius):
    square_limitations = HaversineFormula.calculate_square_limitations(center_longitude, center_latitude, radius)

    max_latitude = square_limitations[0]
    min_latitude = square_limitations[1]
    max_longitude = square_limitations[2]
    min_longitude = square_limitations[3]

    shops = []
    with dataset.connect(*get_database_connection_params()) as database:
        for shop in database['shop']:
            shop_latitude = shop['latitude']
            shop_longitude = shop['longitude']
            if min_longitude <= shop_longitude <= max_longitude and min_latitude <= shop_latitude <= max_latitude:
                shops.append(shop)

    return shops
