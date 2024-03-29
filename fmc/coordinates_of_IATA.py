#!/usr/bin/env python3

# Define function ...
def coordinates_of_IATA(airports, iata, /):
    # Loop over all airports ...
    for airport in airports:
        # Check if this is the correct one and return it's coordinates ...
        if airport["IATA"] == iata:
            return airport["Longitude"], airport["Latitude"]

    # Return defaults if it was not found ...
    return 0.0, 0.0
