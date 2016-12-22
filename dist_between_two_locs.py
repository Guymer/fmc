# -*- coding: utf-8 -*-

def dist_between_two_locs(lon1 = 0.0, lat1 = 0.0, lon2 = 0.0, lat2 = 0.0):
    # Import modules ...
    import math

    # Load sub-functions ...
    from .angle_between_two_locs import angle_between_two_locs

    # Calculate distance in degrees ...
    distance_deg = angle_between_two_locs(lon1, lat1, lon2, lat2)               # [deg]

    # Convert to radians ...
    distance_rad = math.radians(distance_deg)                                   # [rad]

    # Convert to kilometers ...
    # NOTE: Earth's mean radius is 6,371.009 km.
    distance_km = 6371.009 * distance_rad                                       # [km]

    return distance_km
