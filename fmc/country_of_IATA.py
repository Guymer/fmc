#!/usr/bin/env python3

# Define function ...
def country_of_IATA(
    airports,
    iata,
    /,
):
    """Find the country of an airport

    Parameters
    ----------
    airports : list
        the list of all of the airports
    iata : str
        the IATA code of the desired airport

    Returns
    -------
    country : str
        the country of the airport

    Notes
    -----
    Copyright 2016 Thomas Guymer [1]_

    References
    ----------
    .. [1] FMC, https://github.com/Guymer/fmc
    """

    # **************************************************************************

    # Catch special cases ...
    if iata == "TXL":                   # This airport closed on 4/May/2021.
        return "Germany"

    # Loop over all airports ...
    for airport in airports:
        # Skip this airport if it does not have an IATA code ...
        if "IATA" not in airport:
            continue

        # Check if this is the correct one and return it's country ...
        if airport["IATA"] == iata:
            return airport["ISO 3166-1 English Short Name"]

    # Return default if it was not found ...
    return "ERROR"
