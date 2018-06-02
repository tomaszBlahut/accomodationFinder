import numpy
from ..models.search_state import SearchState
from ..models.request_parameters import RequestParameters
from ..shop_dal import get_shop_collection_within_area_bounds
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
            wage = float(wages[shop["name"]])
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

        shops = get_shop_collection_within_area_bounds(request_parameters.area_bounds)

        wages = request_parameters.wages

        try:
            latitude_points, latitude_step = numpy.linspace(
                request_parameters.area_bounds["south"],
                request_parameters.area_bounds["north"],
                request_parameters.mesh_density,
                retstep=True)
            longitude_points, longitude_step = numpy.linspace(
                request_parameters.area_bounds["west"],
                request_parameters.area_bounds["east"],
                request_parameters.mesh_density,
                retstep=True)

            values = numpy.zeros((len(latitude_points),
                                  len(longitude_points)))

            for shop in shops:
                SearchProcessor.calculate_values_for_shop(shop,
                                                          wages,
                                                          latitude_points,
                                                          longitude_points,
                                                          values)

            min_value = numpy.amin(values)
            values = numpy.add(values, -min_value)

            max_value = numpy.amax(values)
            normalized_values = numpy.multiply(values, 1/max_value)

            results = {"values": normalized_values,
                       "latitudes": latitude_points,
                       "longitudes": longitude_points,
                       "mesh_density": request_parameters.mesh_density,
                       "latitude_step": latitude_step,
                       "longitude_step": longitude_step}
            update_search_result_output(id, results)

            update_search_result_status(id, SearchState.COMPLETED)

            return values

        except Exception as exception:
            update_search_result_status(id, SearchState.FAILED)

            results = {"type": str(type(exception)),
                       "args": exception.args,
                       "message": str(exception)}
            update_search_result_output(id, results)            
