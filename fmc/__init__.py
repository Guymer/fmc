#!/usr/bin/env python3

"""
Flight Map Creator (FMC)

This Python 3.x module contains all the functions required to create a map of
the world with all of your flights overlaid and all of the countries that you
have visited shaded in too.
"""

# Import sub-functions ...
from .coordinates_of_IATA import coordinates_of_IATA
from .coordinates_of_ICAO import coordinates_of_ICAO
from .country_of_IATA import country_of_IATA
from .country_of_ICAO import country_of_ICAO
from .load_airport_list import load_airport_list
from .run import run
