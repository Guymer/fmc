"""
Flight Map Creator (FMC)

This Python 3.x module contains all the functions required to create a map of
the world with all of your flights overlaid and all of the countries that you
have visited shaded in too.
"""

# Import standard modules ...
import sys

# Import sub-functions ...
from .calc_horizontal_gridlines import calc_horizontal_gridlines
from .calc_vertical_gridlines import calc_vertical_gridlines
from .coordinates_of_IATA import coordinates_of_IATA
from .country_of_IATA import country_of_IATA
from .load_airport_list import load_airport_list
from .run import run

# Ensure that this module is only imported by Python 3.x ...
if sys.version_info.major != 3:
    raise Exception("the Python module \"fmc\" must only be used with Python 3.x") from None
