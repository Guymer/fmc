#!/usr/bin/env python3

# Define function ...
def coordinates_of_IATA(
    airports,
    iata,
    /,
):
    """Find the longitude and latitude of an airport

    Parameters
    ----------
    airports : list
        the list of all of the airports
    iata : str
        the IATA code of the desired airport

    Returns
    -------
    lon : float
        the longitude of the airport (in degrees)
    lat : float
        the latitude of the airport (in degrees)

    Notes
    -----
    Copyright 2016 Thomas Guymer [1]_

    References
    ----------
    .. [1] FMC, https://github.com/Guymer/fmc
    """

    # **************************************************************************

    # Loop over all airports ...
    for airport in airports:
        # Skip this airport if it does not have an IATA code ...
        if "IATA" not in airport:
            continue

        # Check if this is the correct one and return it's coordinates ...
        if airport["IATA"] == iata:
            return airport["Longitude"], airport["Latitude"]

    # Return defaults if it was not found ...
    return 0.0, 0.0
