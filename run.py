# -*- coding: utf-8 -*-

def run(flightLog = "/this/path/does/not/exist", extraCountries = [], renames = {}):
    # Import modules ...
    import cartopy
    import cartopy.crs
    import cartopy.io.shapereader
    import csv
    import math
    import matplotlib
    # NOTE: http://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server
    matplotlib.use("Agg")
    import matplotlib.image
    import matplotlib.pyplot
    import pyguymer

    # Load sub-functions ...
    from .coordinates_of_IATA import coordinates_of_IATA
    from .country_of_IATA import country_of_IATA
    from .load_airport_list import load_airport_list

    # Create plot and make it pretty ...
    fig = matplotlib.pyplot.figure(
        figsize = (9, 6),
        dpi = 300,
        frameon = False
    )
    ax = matplotlib.pyplot.axes(projection = cartopy.crs.Robinson())
    ax.set_global()
    ax.stock_img()
    ax.coastlines(
        resolution = "10m",
        color = "black",
        linewidth = 0.1
    )

    # Add notable lines of latitude manually ...
    y1 = 66.0 + 33.0 / 60.0 + 46.2 / 3600.0                                     # [deg]
    y2 = 23.0 + 26.0 / 60.0 + 13.8 / 3600.0                                     # [deg]
    matplotlib.pyplot.plot(
        [-180.0, 180.0],
        [ y1,  y1],
        transform = cartopy.crs.PlateCarree(),
        color = "black",
        linewidth = 0.1,
        linestyle = ":"
    )
    matplotlib.pyplot.plot(
        [-180.0, 180.0],
        [ y2,  y2],
        transform = cartopy.crs.PlateCarree(),
        color = "black",
        linewidth = 0.1,
        linestyle = ":"
    )
    matplotlib.pyplot.plot(
        [-180.0, 180.0],
        [0.0, 0.0],
        transform = cartopy.crs.PlateCarree(),
        color = "black",
        linewidth = 0.1,
        linestyle = ":"
    )
    matplotlib.pyplot.plot(
        [-180.0, 180.0],
        [-y2, -y2],
        transform = cartopy.crs.PlateCarree(),
        color = "black",
        linewidth = 0.1,
        linestyle = ":"
    )
    matplotlib.pyplot.plot(
        [-180.0, 180.0],
        [-y1, -y1],
        transform = cartopy.crs.PlateCarree(),
        color = "black",
        linewidth = 0.1,
        linestyle = ":"
    )

    # Load airport list ...
    db = load_airport_list()

    # Create flight dictionary and loop over all flights ...
    flights = {}
    total_dist = 0.0                                                            # [m]
    for row in csv.reader(open(flightLog, "rt")):
        # Extract IATA codes for this flight ...
        iata1 = row[0]
        iata2 = row[1]

        # Skip this flight if the codes are not what I expect ...
        if len(iata1) != 3 or len(iata2) != 3:
            continue

        # Find coordinates for this flight and add it's distance to the total ...
        lon1, lat1 = coordinates_of_IATA(db, iata1)                             # [deg], [deg]
        lon2, lat2 = coordinates_of_IATA(db, iata2)                             # [deg], [deg]
        dist, alpha1, alpha2 = pyguymer.dist_between_two_locs(lon1, lat1, lon2, lat2)    # [m], [deg], [deg]
        total_dist += dist                                                      # [m]

        # Create flight name and skip this flight if it has already been drawn ...
        if iata1 < iata2:
            flight = iata1 + "-" + iata2
        else:
            flight = iata2 + "-" + iata1
        if flight in flights:
            continue
        flights[flight] = True

        # Draw the great circle ...
        matplotlib.pyplot.plot(
            [lon1, lon2],
            [lat1, lat2],
            transform = cartopy.crs.Geodetic(),
            linewidth = 1.0,
            color = "red"
        )

        # Find countries and add them to the list if either are missing ...
        country1 = country_of_IATA(db, iata1)
        country2 = country_of_IATA(db, iata2)
        if country1 not in extraCountries:
            extraCountries.append(country1)
        if country2 not in extraCountries:
            extraCountries.append(country2)

    # Convert m to km ...
    total_dist /= 1000.0                                                        # [km]

    # Add annotation ...
    label = "You have flown {0:,d} km. You have flown around the Earth {1:.1f} times. You have flown to the Moon {2:.1f} times.".format(int(total_dist), total_dist / (2.0 * math.pi * 6371.009), total_dist / 384402.0)
    ax.text(
        0.5,
        -0.02,
        label,
        horizontalalignment = "center",
        verticalalignment = "center",
        transform = ax.transAxes,
        fontsize = 5
    )

    # Clean up the list ...
    # NOTE: The airport database and the country shape database use different
    #       names for some countries. The user may provide a dictionary to
    #       rename countries.
    for country1, country2 in renames.iteritems():
        if country1 in extraCountries:
            extraCountries.remove(country1)
            extraCountries.append(country2)

    # Find file containing all the country shapes ...
    shape_file = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
        category = "cultural",
        name = "admin_0_countries"
    )

    # Loop over records ...
    for record in cartopy.io.shapereader.Reader(shape_file).records():
        # Check if this country is in the list ...
        if record.attributes["NAME"] in extraCountries:
            # Fill the country in and remove it from the list ...
            # NOTE: Removing them from the list enables us to print out the ones
            #       that where not found later on.
            ax.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                alpha = 0.5,
                color = "red",
                facecolor = "red",
                linewidth = 0.1
            )
            extraCountries.remove(record.attributes["NAME"])

    # Save map as PNG ...
    matplotlib.pyplot.savefig(
        flightLog.replace(".csv", ".png"),
        bbox_inches = "tight",
        dpi = 300,
        pad_inches = 0.1
    )
    matplotlib.pyplot.close("all")

    # Print out the countries that were not drawn ...
    for country in extraCountries:
        print "\"{0:s}\" was not drawn.".format(country)
