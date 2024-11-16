#!/usr/bin/env python3

# Define function ...
def coordinates_of_ICAO(
    airports,
    icao,
    /,
):
    """Find the longitude and latitude of an airport

    Parameters
    ----------
    airports : list
        the list of all of the airports
    icao : str
        the ICAO code of the desired airport

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
        # Skip this airport if it does not have an ICAO code ...
        if "ICAO" not in airport:
            continue

        # Check if this is the correct one and return it's coordinates ...
        if airport["ICAO"] == icao:
            return airport["lon"], airport["lat"]

    # Return defaults if it was not found ...
    return 0.0, 0.0
