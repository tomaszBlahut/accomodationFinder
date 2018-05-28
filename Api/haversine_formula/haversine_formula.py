from math import radians, sin, cos, sqrt, asin, atan2, pi, radians, degrees


class HaversineFormula:
    EARTH_RADIUS = 6372800
    RIGHT_ANGLE = 90

    @staticmethod
    def calculate_distance_beetween_two_points(longitude1, longitude2, latitude1, latitude2):
        latitude_distance_radians = radians(latitude2 - latitude1)
        longitude_distance_radians = radians(longitude2 - longitude1)
        latitude1_radians = radians(latitude1)
        latitude2_radians = radians(latitude2)

        inner_hav = sin(latitude_distance_radians / 2) ** 2 + cos(latitude1_radians) * cos(latitude2_radians) * sin(
            longitude_distance_radians / 2) ** 2

        return 2 * HaversineFormula.EARTH_RADIUS * asin(sqrt(inner_hav))

    @staticmethod
    def calculate_square_bounds(longitude, latitude, radius):
        ang_dist = radius / HaversineFormula.EARTH_RADIUS

        latitude = radians(latitude)
        longitude = radians(longitude)

        coordinates_up = HaversineFormula.calculate_end_latitude_and_longitude(latitude, longitude, ang_dist, 0)
        coordinates_right = HaversineFormula.calculate_end_latitude_and_longitude(latitude, longitude, ang_dist, 1)
        coordinates_down = HaversineFormula.calculate_end_latitude_and_longitude(latitude, longitude, ang_dist, 2)
        coordinates_left = HaversineFormula.calculate_end_latitude_and_longitude(latitude, longitude, ang_dist, 3)

        return {"up": {"longitude": degrees(coordinates_up[0]), "latitude": degrees(coordinates_up[1])},
                "right": {"longitude": degrees(coordinates_right[0]), "latitude": degrees(coordinates_right[1])},
                "down": {"longitude": degrees(coordinates_down[0]), "latitude": degrees(coordinates_down[1])},
                "left": {"longitude": degrees(coordinates_left[0]), "latitude": degrees(coordinates_left[1])}}

    @staticmethod
    def calculate_end_latitude(start_latitude, ang_dist, bearing):
        return asin(sin(start_latitude) * cos(ang_dist) + cos(start_latitude) * sin(ang_dist) * cos(bearing))

    @staticmethod
    def calculate_end_longitude(start_latitude, end_latitude, start_longitude, ang_dist, bearing):
        return start_longitude + atan2(sin(bearing) * sin(ang_dist) * cos(start_latitude),
                                       cos(ang_dist) - sin(start_latitude) * sin(end_latitude))

    @staticmethod
    def calculate_end_latitude_and_longitude(start_latitude, start_longitude, ang_dist, bearing_factor):
        bearing = radians(bearing_factor * HaversineFormula.RIGHT_ANGLE)

        end_latitude = HaversineFormula.calculate_end_latitude(start_latitude, ang_dist, bearing)
        end_longitude = HaversineFormula.calculate_end_longitude(start_latitude, end_latitude, start_longitude,
                                                                 ang_dist, bearing)

        return end_longitude, end_latitude
