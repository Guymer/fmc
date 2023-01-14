#!/usr/bin/env python3

# Define function ...
def load_airport_list():
    # Import standard modules ...
    import csv
    import os

    # Create the empty list ...
    airports = []

    # Make database path ...
    dbpath = f"{os.path.dirname(__file__)}/../openflights/data/airports.dat"

    # Check that database is there ...
    if not os.path.exists(dbpath):
        print("INFO: The airport database is missing. It is included as a ")
        print("      submodule in Git. If you did not clone this repository with")
        print("      the \"--recursive\" option then you can still pull down the")
        print("      submodule by running \"git submodule update --init\" now.")
        raise Exception("the airport database is missing") from None

    # Open database ...
    with open(dbpath, "rt", encoding = "utf-8") as fObj:
        # Loop over all airports ...
        for row in csv.reader(fObj):
            # Load string parameters ...
            tmp = {
                      "Name" : row[ 1],
                      "City" : row[ 2],
                   "Country" : row[ 3],
                      "IATA" : row[ 4],
                      "ICAO" : row[ 5],
                "DST-scheme" : row[10],
                   "TZ-name" : row[11]
            }

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

    # Return the full list ...
    return airports
