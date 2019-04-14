# -*- coding: utf-8 -*-

def coordinates_of_IATA(airports, iata):
    # Check if the airport is in the database ...
    if iata in airports:
        # Return it's coordinates ...
        return airports[iata][u"Longitude"], airports[iata][u"Latitude"]
    else:
        print u"WARNING: {0:s} is not in the airport database".format(iata)

        # Return defaults if it was not found ...
        return 0.0, 0.0
