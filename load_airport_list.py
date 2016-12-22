# -*- coding: utf-8 -*-

def load_airport_list():
    # NOTE: The airport database was obtained from:
    # NOTE:   * https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat

    # Import modules ...
    import csv
    import io
    import os

    # Create the empty list ...
    airports = []

    # Make database path ...
    dbpath = os.path.join(os.path.dirname(__file__), "airports.csv")

    # Open CSV database ...
    # HACK: The Python 2.X "csv" module does not natively handle unicode
    #       characters so I strip them out using this ugly "io" function call.
    with io.open(dbpath, mode = "rt", encoding = "ascii", errors = "ignore") as fobj:
        # Loop over all airports and append a dictionary to the list ...
        for row in csv.reader(fobj):
            airports.append(
                {
                    "ID": int(row[0]),
                    "Name": row[1],
                    "City": row[2],
                    "Country": row[3],
                    "IATA": row[4],
                    "ICAO": row[5],
                    "Latitude": float(row[6]),
                    "Longitude": float(row[7]),
                    "Altitude": float(row[8]),
                    "UTC-offset": float(row[9]),
                    "DST-scheme": row[10],
                    "TZ-name": row[11]
                }
            )

    # Return the full list ...
    return airports
