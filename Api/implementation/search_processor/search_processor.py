import numpy
from ..models.search_state import SearchState
from ..models.request_parameters import RequestParameters
from ..haversine_formula.haversine_formula import HaversineFormula
from ..shop_dal import get_shop_collection_within_range
from ..search_results_dal import update_search_result_status, update_search_result_output


class SearchProcessor:
    @staticmethod
    def calculate_values_for_shop(shop, wages, latitudes, longitudes, values):
        latitude_index = (numpy.abs(latitudes - shop["latitude"])).argmin()
        longitude_index = (numpy.abs(longitudes - shop["longitude"])).argmin()

        max_latitude_points = max((latitude_index,
                                   len(latitudes) - latitude_index)) + 1
        max_longitude_points = max((longitude_index,
                                   len(longitudes) - longitude_index)) + 1

        wage = 1.0
        try:
            wage = wages[shop["name"]]
        except KeyError:
            pass

        for y in range(1, max_longitude_points):
            can_add = longitude_index + y < len(longitudes)
            can_substract = longitude_index - y >= 0
            value = y * wage
            for z in range(len(latitudes)):
                if can_add:
                    values[z, longitude_index + y] += value
                if can_substract:
                    values[z, longitude_index - y] += value

        for x in range(1, max_latitude_points):
            can_add = latitude_index + x < len(latitudes)
            can_substract = latitude_index - x >= 0
            value = x * wage
            for z in range(len(longitudes)):
                if can_add:
                    values[latitude_index + x, z] += value
                if can_substract:
                    values[latitude_index - x, z] += value

    @staticmethod
    def process_search(id, json_request_parameters):
        update_search_result_status(id, SearchState.PROCESSING)

        request_parameters = RequestParameters(json_request_parameters)

        shops = get_shop_collection_within_range(request_parameters.start["longitude"],
                                                 request_parameters.start["latitude"],
                                                 request_parameters.radius)
        wages = request_parameters.wages

        try:
            square_bounds = HaversineFormula.calculate_square_bounds(
                request_parameters.start["longitude"],
                request_parameters.start["latitude"],
                request_parameters.radius)

            latitude_points = numpy.linspace(
                square_bounds["up"]["latitude"],
                square_bounds["down"]["latitude"],
                request_parameters.mesh_density)
            longitude_points = numpy.linspace(
                square_bounds["left"]["longitude"],
                square_bounds["right"]["longitude"],
                request_parameters.mesh_density)

            values = numpy.zeros((len(latitude_points),
                                  len(longitude_points)))

            for shop in shops:
                SearchProcessor.calculate_values_for_shop(shop,
                                                          wages,
                                                          latitude_points,
                                                          longitude_points,
                                                          values)

            results = {"values": values,
                       "latitudes": latitude_points,
                       "longitudes": longitude_points,
                       "mesh_density": request_parameters.mesh_density}
            update_search_result_output(id, results)

            update_search_result_status(id, SearchState.COMPLETED)

            return values

        except Exception as exception:
            results = {"type": str(type(exception)),
                       "args": exception.args,
                       "message": str(exception)}
            update_search_result_output(id, results)

            update_search_result_status(id, SearchState.FAILED)
