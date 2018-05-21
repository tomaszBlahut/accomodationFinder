from math import radians, sin, cos, sqrt, asin, atan2, pi, radians, degrees


class HaversineFormula:
    earth_radius = 6372800

    @staticmethod
    def calculate_distance_beetween_two_points(longitude1, longitude2, latitude1, latitude2):
        latitude_distance_radians = radians(latitude2 - latitude1)
        longitude_distance_radians = radians(longitude2 - longitude1)
        latitude1_radians = radians(latitude1)
        latitude2_radians = radians(latitude2)

        inner_hav = sin(latitude_distance_radians / 2) ** 2 + cos(latitude1_radians) * cos(latitude2_radians) * sin(
            longitude_distance_radians / 2) ** 2

        return 2 * HaversineFormula.earth_radius * asin(sqrt(inner_hav))

    @staticmethod
    def calculate_square_bounds(longitude, latitude, radius):
        ang_dist = radius / HaversineFormula.earth_radius

        latitude = radians(latitude)
        longitude = radians(longitude)

        bearing = radians(0)
        latitude_up = asin(sin(latitude) * cos(ang_dist) + cos(latitude) * sin(ang_dist) * cos(bearing))
        longitude_up = longitude + atan2(sin(bearing) * sin(ang_dist) * cos(latitude),
                                         cos(ang_dist) - sin(latitude) * sin(latitude_up))

        bearing = radians(90)
        latitude_right = asin(sin(latitude) * cos(ang_dist) + cos(latitude) * sin(ang_dist) * cos(bearing))
        longitude_right = longitude + atan2(sin(bearing) * sin(ang_dist) * cos(latitude),
                                            cos(ang_dist) - sin(latitude) * sin(latitude_right))

        bearing = radians(180)
        latitude_down = asin(sin(latitude) * cos(ang_dist) + cos(latitude) * sin(ang_dist) * cos(bearing))
        longitude_down = longitude + atan2(sin(bearing) * sin(ang_dist) * cos(latitude),
                                           cos(ang_dist) - sin(latitude) * sin(latitude_down))

        bearing = radians(270)
        latitude_left = asin(sin(latitude) * cos(ang_dist) + cos(latitude) * sin(ang_dist) * cos(bearing))
        longitude_left = longitude + atan2(sin(bearing) * sin(ang_dist) * cos(latitude),
                                           cos(ang_dist) - sin(latitude) * sin(latitude_left))

        return {"up": {"longitude": degrees(longitude_up), "latitude": degrees(latitude_up)},
                "right": {"longitude": degrees(longitude_right), "latitude": degrees(latitude_right)},
                "down": {"longitude": degrees(longitude_down), "latitude": degrees(latitude_down)},
                "left": {"longitude": degrees(longitude_left), "latitude": degrees(latitude_left)}}
