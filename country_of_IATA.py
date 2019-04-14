# -*- coding: utf-8 -*-

def country_of_IATA(airports, iata):
    # Import modules ...
    import cartopy

    # Check if the airport is in the database ...
    if iata in airports:
        # Find file containing all the countries ...
        sfile = cartopy.io.shapereader.natural_earth(
            resolution = u"10m",
              category = u"cultural",
                  name = u"admin_0_countries"
        )

        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(sfile).records():
            # Loop over geometries ...
            for geometry in record.geometry:
                # Check if this airport is in this geometry ...
                if geometry.contains(airports[iata][u"Point"]):
                    # Return it's country ...
                    return record.attributes[u"NAME"]

        print u"WARNING: {0:s} was not found in a country".format(iata)

        # Return defaults if it was not found ...
        return u"ERROR"
    else:
        print u"WARNING: {0:s} is not in the airport database".format(iata)

        # Return defaults if it was not found ...
        return u"ERROR"
