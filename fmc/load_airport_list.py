#!/usr/bin/env python3

# Define function ...
def load_airport_list(
    *,
      dat = "airports.dat",
    debug = __debug__,
):
    """Load the airport database

    This function reads in a CSV from OpenFlights, parses all of the columns
    (converting them to the appropriate data type) and then returns a list of
    all of the airports.

    Parameters
    ----------
    dat : str, option
        the CSV to load (at time of writing, only "airports.dat" and
        "airports-extended.dat" will work)
    debug : bool, optional
        print debug messages

    Returns
    -------
    airports : list
        the list of all of the airports

    Notes
    -----
    Copyright 2016 Thomas Guymer [1]_

    References
    ----------
    .. [1] FMC, https://github.com/Guymer/fmc
    """

    # Import standard modules ...
    import csv
    import os

    # **************************************************************************

    # Create short-hand ...
    datPath = f"{os.path.dirname(__file__)}/../openflights/data/{dat}"

    # Check that database is there ...
    if not os.path.exists(datPath):
        print("INFO: The airport database is missing. It is included as a ")
        print("      submodule in Git. If you did not clone this repository with")
        print("      the \"--recursive\" option then you can still pull down the")
        print("      submodule by running \"git submodule update --init\" now.")
        raise Exception("the airport database is missing") from None

    # **************************************************************************

    # Create the empty list ...
    airports = []

    # Open database ...
    with open(datPath, "rt", encoding = "utf-8") as fObj:
        # Loop over all airports ...
        for row in csv.reader(fObj):
            # Load string parameters and remove blank ones ...
            tmp = {
                      "Name" : row[ 1],
                      "City" : row[ 2],
                   "Country" : row[ 3],
                      "IATA" : row[ 4],
                      "ICAO" : row[ 5],
                "DST-scheme" : row[10],
                   "TZ-name" : row[11],
            }
            if tmp["IATA"] == "\\N":
                del tmp["IATA"]
            if tmp["ICAO"] == "\\N":
                del tmp["ICAO"]

            # Try loading numeric parameter ...
            try:
                tmp["ID"] = int(row[0])
            except ValueError:
                pass

            # Try loading numeric parameter ...
            try:
                tmp["Latitude"] = float(row[6])                                 # [°]
            except ValueError:
                pass

            # Try loading numeric parameter ...
            try:
                tmp["Longitude"] = float(row[7])                                # [°]
            except ValueError:
                pass

            # Try loading numeric parameter ...
            try:
                tmp["Altitude"] = float(row[8])                                 # [ft]
            except ValueError:
                pass

            # Try loading numeric parameter ...
            try:
                tmp["UTC-offset"] = float(row[9])                               # [hr]
            except ValueError:
                pass

            # Append dictionary to the list ...
            airports.append(tmp)

    # **************************************************************************

    # Check if the user wants to check the data ...
    if debug:
        # Check if any two airports have the same IATA code ...
        iatas = []
        for airport in airports:
            if "IATA" not in airport:
                continue
            if airport["IATA"] in iatas:
                raise Exception(f'two airports have the IATA code of \"{airport["IATA"]}\"') from None
            iatas.append(airport["IATA"])
        del iatas

        # Check if any two airports have the same ICAO code ...
        icaos = []
        for airport in airports:
            if "ICAO" not in airport:
                continue
            if airport["ICAO"] in icaos:
                raise Exception(f'two airports have the ICAO code of \"{airport["ICAO"]}\"') from None
            icaos.append(airport["ICAO"])
        del icaos

    # **************************************************************************

    # Return the full list ...
    return airports
