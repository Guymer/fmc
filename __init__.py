# -*- coding: utf-8 -*-

"""
Flight Map Creator (FMC)

This module contains all the functions required to create a map of the world
with all of your flights overlaid and all of the countries that you have visited
shaded in too.
"""

# Load sub-functions ...
from .angle_between_two_locs import angle_between_two_locs
from .coordinates_of_IATA import coordinates_of_IATA
from .country_of_IATA import country_of_IATA
from .dist_between_two_locs import dist_between_two_locs
from .load_airport_list import load_airport_list
from .run import run
