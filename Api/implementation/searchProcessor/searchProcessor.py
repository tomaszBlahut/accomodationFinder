from .searchState import SearchState
from math import cos
import numpy
from ..haversine_formula.haversine_formula import HaversineFormula


class Expandable:
    pass


class SearchProcessor:
    @staticmethod
    def change_search_state(id, state):
        print(str(state))

    @staticmethod
    def calculate_values_for_shop(shop, latitudes, longitudes, values):
        latitude_index = (numpy.abs(latitudes - shop.latitude)).argmin()
        longitude_index = (numpy.abs(longitudes - shop.longitude)).argmin()

        max_latitude_points = max((latitude_index,
                                   len(latitudes) - latitude_index)) + 1
        max_longitude_points = max((longitude_index,
                                   len(longitudes) - longitude_index)) + 1

        for y in range(1, max_longitude_points):
            can_add = longitude_index + y < len(longitudes)
            can_substract = longitude_index - y >= 0
            for z in range(len(latitudes)):
                if can_add:
                    values[z, longitude_index + y] += y
                if can_substract:
                    values[z, longitude_index - y] += y

        for x in range(1, max_latitude_points):
            can_add = latitude_index + x < len(latitudes)
            can_substract = latitude_index - x >= 0
            for z in range(len(longitudes)):
                if can_add:
                    values[latitude_index + x, z] += x
                if can_substract:
                    values[latitude_index - x, z] += x

    @staticmethod
    def process_search(id, request_parameters):
        SearchProcessor.change_search_state(id, SearchState.PROCESSING)

        # get shops from endpoint
        shop1 = Expandable()
        shop2 = Expandable()
        shop1.latitude = 50.1
        shop2.latitude = 49.8
        shop1.longitude = 22.1
        shop2.longitude = 22.4
        shops = []
        shops.append(shop1)
        shops.append(shop2)

        try:
            meters_in_latitude = 111.32 * 1000
            meters_in_longitude = 40075 * 1000
            cos_of_start_angle = cos(request_parameters.start.longitude)
            latitude_meter = 1 / meters_in_latitude
            longitude_meter = 1 / (meters_in_longitude * cos_of_start_angle)

            square_bounds = HaversineFormula.calculate_square_bounds(
                request_parameters.start.longitude,
                request_parameters.start.latitude,
                request_parameters.radius)

            latitude_points = numpy.linspace(
                square_bounds["up"]["latitude"],
                square_bounds["down"]["latitude"],
                request_parameters.mesh_density)
            longitude_points = numpy.linspace(
                square_bounds["left"]["longitude"],
                square_bounds["right"]["longitude"],
                request_parameters.mesh_density)

            latitudes, longitudes = numpy.meshgrid(latitude_points,
                                                   longitude_points)

            values = numpy.zeros((len(latitude_points),
                                  len(longitude_points)))

            for shop in shops:
                SearchProcessor.calculate_values_for_shop(shop,
                                                          latitude_points,
                                                          longitude_points,
                                                          values)

            results = []

            for x in range(len(values)):
                row = []
                for y in range(len(values[x])):
                    result_object = (latitude_points[x],
                                     longitude_points[y],
                                     values[x, y])
                    row.append(result_object)
                results.append(row)

            # set results mesh into DB

            SearchProcessor.change_search_state(id, SearchState.COMPLETED)

            return values

        except AssertionError:
            SearchProcessor.change_search_state(id, SearchState.FAILED)
