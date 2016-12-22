# -*- coding: utf-8 -*-

def angle_between_two_locs(lon1 = 0.0, lat1 = 0.0, lon2 = 0.0, lat2 = 0.0):
    # Import modules ...
    import math

    # Convert to radians ...
    lon1_rad = math.radians(lon1)                                               # [rad]
    lat1_rad = math.radians(lat1)                                               # [rad]
    lon2_rad = math.radians(lon2)                                               # [rad]
    lat2_rad = math.radians(lat2)                                               # [rad]

    # Calculate angle in radians ...
    distance_rad = 2.0 * math.asin(math.sqrt(math.pow((math.sin((lat1_rad - lat2_rad) / 2.0)), 2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.pow((math.sin((lon1_rad - lon2_rad) / 2.0)), 2)))    # [rad]

    # Convert to degrees ...
    distance_deg = math.degrees(distance_rad)                                   # [deg]

    return distance_deg
