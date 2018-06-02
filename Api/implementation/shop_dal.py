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


def get_shop_collection_within_area_bounds(area_bounds):
    max_latitude = area_bounds["north"]
    min_latitude = area_bounds["south"]
    max_longitude = area_bounds["east"]
    min_longitude = area_bounds["west"]

    shops_collection = []
    with dataset.connect(*get_database_connection_params()) as database:
        table = database['shop']
        shops = table.find(min_longitude <= table.table.columns.longitude, table.table.columns.longitude <= max_longitude, min_latitude <= table.table.columns.latitude, table.table.columns.latitude <= max_latitude)
        shops_collection = [*shops]

    return shops_collection


def get_shop_names_within_area_bounds(area_bounds):
    max_latitude = area_bounds["north"]
    min_latitude = area_bounds["south"]
    max_longitude = area_bounds["east"]
    min_longitude = area_bounds["west"]

    with dataset.connect(*get_database_connection_params()) as database:
        table = database['shop']
        shops = table.distinct('name', min_longitude <= table.table.columns.longitude, table.table.columns.longitude <= max_longitude, min_latitude <= table.table.columns.latitude, table.table.columns.latitude <= max_latitude)
        types_of_shops = [*shops]

    return types_of_shops


def get_all_shop_types():
    with dataset.connect(*get_database_connection_params()) as database:
        shops = database['shop'].distinct('name')
        types_of_shops = [*shops]

    return types_of_shops
