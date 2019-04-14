# -*- coding: utf-8 -*-

def load_airport_list():
    # Import modules ...
    import cartopy

    print u"Finding airports ..."

    # Create the empty dictionary ...
    airports = {}

    # Find file containing all the airports ...
    sfile = cartopy.io.shapereader.natural_earth(
        resolution = u"10m",
          category = u"cultural",
              name = u"airports"
    )

    # Loop over records ...
    for record in cartopy.io.shapereader.Reader(sfile).records():
        # Add airport to dictionary ...
        airports[record.attributes[u"iata_code"]] = {
            u"Longitude" : record.geometry.x,
            u"Latitude" : record.geometry.y,
            u"Point" : record.geometry,
            u"Name" : record.attributes[u"name_en"]
        }

    # Return the full list ...
    return airports
