# -*- coding: utf-8 -*-

def run(flightLog = "/this/path/does/not/exist", extraCountries = [], renames = {}):
    # Import modules ...
    import cartopy
    import cartopy.crs
    import cartopy.io.shapereader
    import csv
    import datetime
    import math
    import matplotlib
    matplotlib.use("Agg")                                                       # NOTE: http://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server
    import matplotlib.image
    import matplotlib.pyplot
    import pyguymer

    # Load sub-functions ...
    from .coordinates_of_IATA import coordinates_of_IATA
    from .country_of_IATA import country_of_IATA
    from .load_airport_list import load_airport_list

    # Configure matplotlib ...
    matplotlib.pyplot.rcParams.update({"font.size" : 8})

    # Create plot and make it pretty ...
    fig = matplotlib.pyplot.figure(
        figsize = (12, 8),
            dpi = 300,
        frameon = False
    )
    axt = matplotlib.pyplot.subplot2grid(
        (3, 3),
        (0, 0),
        projection = cartopy.crs.Robinson(),
           colspan = 3,
           rowspan = 2
    )
    axl = matplotlib.pyplot.subplot2grid(
        (3, 3),
        (2, 0),
        projection = cartopy.crs.PlateCarree()
    )
    axm = matplotlib.pyplot.subplot2grid(
        (3, 3),
        (2, 1)
    )
    axr = matplotlib.pyplot.subplot2grid(
        (3, 3),
        (2, 2),
        projection = cartopy.crs.PlateCarree()
    )
    axt.set_global()
    axl.set_extent(
        [
            -125.0, # left
             -65.0, # right
              20.0, # bottom
              60.0  # top
        ]
    )
    axr.set_extent(
        [
            -15.0, # left
             45.0, # right
             33.0, # bottom
             73.0  # top
        ]
    )
    pyguymer.add_map_background(axt, resolution = "medium2048px")
    pyguymer.add_map_background(axl, resolution = "medium2048px")
    pyguymer.add_map_background(axr, resolution = "medium2048px")
    axt.coastlines(
        resolution = "10m",
             color = "black",
         linewidth = 0.1
    )
    axl.coastlines(
        resolution = "10m",
             color = "black",
         linewidth = 0.1
    )
    axr.coastlines(
        resolution = "10m",
             color = "black",
         linewidth = 0.1
    )

    # Add notable lines of latitude manually ...
    y1 = 66.0 + 33.0 / 60.0 + 46.2 / 3600.0                                     # [deg]
    y2 = 23.0 + 26.0 / 60.0 + 13.8 / 3600.0                                     # [deg]
    axt.plot(
        [-180.0, 180.0],
        [ y1,  y1],
        transform = cartopy.crs.PlateCarree(),
            color = "black",
        linewidth = 0.5,
        linestyle = ":"
    )
    axt.plot(
        [-180.0, 180.0],
        [ y2,  y2],
        transform = cartopy.crs.PlateCarree(),
            color = "black",
        linewidth = 0.5,
        linestyle = ":"
    )
    axt.plot(
        [-180.0, 180.0],
        [0.0, 0.0],
        transform = cartopy.crs.PlateCarree(),
            color = "black",
        linewidth = 0.5,
        linestyle = ":"
    )
    axt.plot(
        [-180.0, 180.0],
        [-y2, -y2],
        transform = cartopy.crs.PlateCarree(),
            color = "black",
        linewidth = 0.5,
        linestyle = ":"
    )
    axt.plot(
        [-180.0, 180.0],
        [-y1, -y1],
        transform = cartopy.crs.PlateCarree(),
            color = "black",
        linewidth = 0.5,
        linestyle = ":"
    )

    # Add notable lines manually ...
    for xloc in [-120.0, -110.0, -100.0, -90.0, -80.0, -70.0]:
        axl.plot(
            [xloc, xloc],
            [-90.0, 90.0],
            transform = cartopy.crs.PlateCarree(),
                color = "black",
            linewidth = 0.5,
            linestyle = ":"
        )
    for yloc in [20.0, 30.0, 40.0, 50.0, 60.0]:
        axl.plot(
            [-180.0, 180.0],
            [yloc, yloc],
            transform = cartopy.crs.PlateCarree(),
                color = "black",
            linewidth = 0.5,
            linestyle = ":"
        )

    # Add notable lines manually ...
    for xloc in [-10.0, 0.0, 10.0, 20.0, 30.0, 40.0]:
        axr.plot(
            [xloc, xloc],
            [-90.0, 90.0],
            transform = cartopy.crs.PlateCarree(),
                color = "black",
            linewidth = 0.5,
            linestyle = ":"
        )
    for yloc in [40.0, 50.0, 60.0, 70.0]:
        axr.plot(
            [-180.0, 180.0],
            [yloc, yloc],
            transform = cartopy.crs.PlateCarree(),
                color = "black",
            linewidth = 0.5,
            linestyle = ":"
        )

    # Load airport list ...
    db = load_airport_list()

    # Initizalize flight dictionary, histograms and total distance ...
    flights = {}
    businessX = []
    businessY = []
    pleasureX = []
    pleasureY = []
    total_dist = 0.0                                                            # [km]

    # Loop over all flights ...
    for row in csv.reader(open(flightLog, "rt")):
        # Extract IATA codes for this flight ...
        iata1 = row[0]
        iata2 = row[1]

        # Skip this flight if the codes are not what I expect ...
        if len(iata1) != 3 or len(iata2) != 3:
            continue

        # Check if this is the first line ...
        if businessX == []:
            # Loop over the full range of years ...
            for year in xrange(int(row[2][0:4]), int(datetime.date.today().strftime("%Y")) + 1):
                # NOTE: This is a bit of a hack, I should really use NumPy but I
                #       do not want to bring in another dependency that people
                #       may not have.
                businessX.append(year - 0.25)
                businessY.append(0.0)                                           # [km]
                pleasureX.append(year + 0.25)
                pleasureY.append(0.0)                                           # [km]

        # Find coordinates for this flight ...
        lon1, lat1 = coordinates_of_IATA(db, iata1)                             # [deg], [deg]
        lon2, lat2 = coordinates_of_IATA(db, iata2)                             # [deg], [deg]
        dist, alpha1, alpha2 = pyguymer.calc_dist_between_two_locs(lon1, lat1, lon2, lat2)    # [m], [deg], [deg]

        # Convert m to km ...
        dist /= 1000.0                                                          # [km]

        # Add it's distance to the total ...
        total_dist += dist                                                      # [km]

        # Add it's distance to the histogram ...
        if row[3].lower() == "business":
            businessY[businessX.index(int(row[2][0:4]) - 0.25)] += dist         # [km]
        elif row[3].lower() == "pleasure":
            pleasureY[pleasureX.index(int(row[2][0:4]) + 0.25)] += dist         # [km]

        # Create flight name and skip this flight if it has already been drawn ...
        if iata1 < iata2:
            flight = iata1 + "-" + iata2
        else:
            flight = iata2 + "-" + iata1
        if flight in flights:
            continue
        flights[flight] = True

        # Draw the great circle ...
        axt.plot(
            [lon1, lon2],
            [lat1, lat2],
            transform = cartopy.crs.Geodetic(),
            linewidth = 1.0,
                color = "red"
        )
        axl.plot(
            [lon1, lon2],
            [lat1, lat2],
            transform = cartopy.crs.Geodetic(),
            linewidth = 1.0,
                color = "red"
        )
        axr.plot(
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

    # Plot histograms ...
    axm.bar(businessX, businessY, width = 0.45, label = "Business")
    axm.bar(pleasureX, pleasureY, width = 0.45, label = "Pleasure")
    axm.legend()
    axm.set_ylabel("Distance [km/year]")
    axm.xaxis.grid(True)
    axm.yaxis.grid(True)

    # Add annotation ...
    label = "You have flown {0:,d} km. You have flown around the Earth {1:.1f} times. You have flown to the Moon {2:.1f} times.".format(int(total_dist), total_dist / (2.0 * math.pi * 6371.009), total_dist / 384402.0)
    axt.text(
        0.5,
        -0.02,
        label,
        horizontalalignment = "center",
          verticalalignment = "center",
                  transform = axt.transAxes,
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
            axt.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                    alpha = 0.5,
                    color = "red",
                facecolor = "red",
                linewidth = 0.5
            )
            axl.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                    alpha = 0.5,
                    color = "red",
                facecolor = "red",
                linewidth = 0.5
            )
            axr.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                    alpha = 0.5,
                    color = "red",
                facecolor = "red",
                linewidth = 0.5
            )
            extraCountries.remove(record.attributes["NAME"])
        else:
            # Outline the country ...
            axt.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                    alpha = 0.5,
                    color = "black",
                facecolor = "none",
                linewidth = 0.5
            )
            axl.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                    alpha = 0.5,
                    color = "black",
                facecolor = "none",
                linewidth = 0.5
            )
            axr.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                    alpha = 0.5,
                    color = "black",
                facecolor = "none",
                linewidth = 0.5
            )

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
