# -*- coding: utf-8 -*-

"""
Flight Map Creator (FMC)

This module contains all the functions required to create a map of the world
with all of your flights overlaid and all of the countries that you have visited
shaded in too.
"""

# Load sub-functions ...
from .calc_horizontal_gridlines import calc_horizontal_gridlines
from .calc_vertical_gridlines import calc_vertical_gridlines
from .coordinates_of_IATA import coordinates_of_IATA
from .country_of_IATA import country_of_IATA
from .load_airport_list import load_airport_list
from .run import run
