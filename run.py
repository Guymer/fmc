def run(flightLog = "/this/path/does/not/exist", extraCountries = [], renames = {}):
    # Import standard modules ...
    import csv
    import datetime
    import math

    # Import special modules ...
    try:
        import cartopy
        import cartopy.crs
        import cartopy.io.shapereader
    except:
        raise Exception("run \"pip install --user cartopy\"")
    try:
        import matplotlib
        matplotlib.use("Agg")                                                   # NOTE: http://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server
        import matplotlib.image
        import matplotlib.pyplot
    except:
        raise Exception("run \"pip install --user matplotlib\"")

    # Import my modules ...
    try:
        import pyguymer3
    except:
        raise Exception("you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH")

    # Import sub-functions ...
    from .calc_horizontal_gridlines import calc_horizontal_gridlines
    from .calc_vertical_gridlines import calc_vertical_gridlines
    from .coordinates_of_IATA import coordinates_of_IATA
    from .country_of_IATA import country_of_IATA
    from .load_airport_list import load_airport_list

    # Configure matplotlib ...
    matplotlib.pyplot.rcParams.update({"font.size" : 8})

    # Set extents of the two sub-plots ...
    extl = [
        -120.0, # left
         -70.0, # right
          17.0, # bottom
          55.0  # top
    ]
    extr = [
        -10.0, # left
         40.0, # right
         33.0, # bottom
         71.0  # top
    ]

    # Set the half-width of the bars on the histogram ...
    hw = 0.2

    # Create plot and make it pretty ...
    fig = matplotlib.pyplot.figure(figsize = (8, 12), dpi = 300)
    axt = matplotlib.pyplot.subplot2grid(
        (29, 20),
        ( 0,  0),
        projection = cartopy.crs.Robinson(),
           colspan = 20,
           rowspan = 10
    )
    axl = matplotlib.pyplot.subplot2grid(
        (29, 20),
        (10,  0),
        projection = cartopy.crs.Orthographic(
            central_longitude = 0.5 * (extl[0] + extl[1]),
             central_latitude = 0.5 * (extl[2] + extl[3])
        ),
        colspan = 10,
        rowspan =  9
    )
    axr = matplotlib.pyplot.subplot2grid(
        (29, 20),
        (10, 10),
        projection = cartopy.crs.Orthographic(
            central_longitude = 0.5 * (extr[0] + extr[1]),
             central_latitude = 0.5 * (extr[2] + extr[3])
        ),
        colspan = 10,
        rowspan =  9
    )
    axb = matplotlib.pyplot.subplot2grid(
        (29, 20),
        (19,  0),
        colspan = 20,
        rowspan = 10
    )
    axt.set_global()
    axl.set_extent(extl)
    axr.set_extent(extr)
    pyguymer3.add_map_background(axt, resolution = "medium4096px")
    pyguymer3.add_map_background(axl, resolution = "medium4096px")
    pyguymer3.add_map_background(axr, resolution = "medium4096px")
    axt.coastlines(resolution = "10m", color = "black", linewidth = 0.1)
    axl.coastlines(resolution = "10m", color = "black", linewidth = 0.1)
    axr.coastlines(resolution = "10m", color = "black", linewidth = 0.1)

    # Add notable lines of latitude manually (top) ...
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

    # Add notable lines manually (left) ...
    for xloc in range(int(round(extl[0])), int(round(extl[1])) + 1):
        if xloc % 10 != 0:
            continue
        xlocs, ylocs = calc_vertical_gridlines(xloc, extl)
        axl.plot(
            xlocs,
            ylocs,
            transform = cartopy.crs.PlateCarree(),
                color = "black",
            linewidth = 0.5,
            linestyle = ":"
        )
    for yloc in range(int(round(extl[2])), int(round(extl[3])) + 1):
        if yloc % 10 != 0:
            continue
        xlocs, ylocs = calc_horizontal_gridlines(yloc, extl)
        axl.plot(
            xlocs,
            ylocs,
            transform = cartopy.crs.PlateCarree(),
                color = "black",
            linewidth = 0.5,
            linestyle = ":"
        )

    # Add notable lines manually (right) ...
    for xloc in range(int(round(extr[0])), int(round(extr[1])) + 1):
        if xloc % 10 != 0:
            continue
        xlocs, ylocs = calc_vertical_gridlines(xloc, extr)
        axr.plot(
            xlocs,
            ylocs,
            transform = cartopy.crs.PlateCarree(),
                color = "black",
            linewidth = 0.5,
            linestyle = ":"
        )
    for yloc in range(int(round(extr[2])), int(round(extr[3])) + 1):
        if yloc % 10 != 0:
            continue
        xlocs, ylocs = calc_horizontal_gridlines(yloc, extr)
        axr.plot(
            xlocs,
            ylocs,
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
    businessY = []                                                              # [1000 km]
    pleasureX = []
    pleasureY = []                                                              # [1000 km]
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
            for year in range(int(row[2][0:4]), int(datetime.date.today().strftime("%Y")) + 1):
                # NOTE: This is a bit of a hack, I should really use NumPy but I
                #       do not want to bring in another dependency that people
                #       may not have.
                businessX.append(year - hw)
                businessY.append(0.0)                                           # [1000 km]
                pleasureX.append(year + hw)
                pleasureY.append(0.0)                                           # [1000 km]

        # Find coordinates for this flight ...
        lon1, lat1 = coordinates_of_IATA(db, iata1)                             # [deg], [deg]
        lon2, lat2 = coordinates_of_IATA(db, iata2)                             # [deg], [deg]
        dist, alpha1, alpha2 = pyguymer3.calc_dist_between_two_locs(lon1, lat1, lon2, lat2)    # [m], [deg], [deg]

        # Convert m to km ...
        dist *= 0.001                                                           # [km]

        # Add it's distance to the total ...
        total_dist += dist                                                      # [km]

        # Add it's distance to the histogram ...
        if row[3].lower() == "business":
            businessY[businessX.index(int(row[2][0:4]) - hw)] += 0.001 * dist   # [1000 km]
        elif row[3].lower() == "pleasure":
            pleasureY[pleasureX.index(int(row[2][0:4]) + hw)] += 0.001 * dist   # [1000 km]

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
    axb.bar(businessX, businessY, width = 2.0 * hw, label = "Business")
    axb.bar(pleasureX, pleasureY, width = 2.0 * hw, label = "Pleasure")
    axb.legend()
    axb.set_ylabel("Distance [1000 km/year]")
    axb.xaxis.grid(True)
    axb.yaxis.grid(True)

    # Add annotation ...
    label = (
        "You have flown {:,d} km. "
        "You have flown around the Earth {:.1f} times. "
        "You have flown to the Moon {:.1f} times."
    ).format(int(total_dist), total_dist / (2.0 * math.pi * 6371.009), total_dist / 384402.0)
    axt.text(
        0.5,
        -0.02,
        label,
        horizontalalignment = "center",
          verticalalignment = "center",
                  transform = axt.transAxes,
                   fontsize = 6
    )

    # Clean up the list ...
    # NOTE: The airport database and the country shape database use different
    #       names for some countries. The user may provide a dictionary to
    #       rename countries.
    for country1, country2 in renames.items():
        if country1 in extraCountries:
            extraCountries.remove(country1)
            extraCountries.append(country2)

    # Find file containing all the country shapes ...
    shape_file = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
          category = "cultural",
              name = "admin_0_countries"
    )

    # Initizalize visited list ...
    visited = []

    # Loop over records ...
    for record in cartopy.io.shapereader.Reader(shape_file).records():
        # Check if this country is in the list ...
        if record.attributes["NAME"] in extraCountries:
            # Append country name to visited list ...
            visited.append(record.attributes["NAME"])

            # Fill the country in and remove it from the list ...
            # NOTE: Removing them from the list enables us to print out the ones
            #       that where not found later on.
            axt.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 1.0),
                facecolor = (1.0, 0.0, 0.0, 0.5),
                linewidth = 0.5
            )
            axl.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 1.0),
                facecolor = (1.0, 0.0, 0.0, 0.5),
                linewidth = 0.5
            )
            axr.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 1.0),
                facecolor = (1.0, 0.0, 0.0, 0.5),
                linewidth = 0.5
            )
            extraCountries.remove(record.attributes["NAME"])
        else:
            # Outline the country ...
            axt.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 1.0),
                facecolor = (0.0, 0.0, 0.0, 0.0),
                linewidth = 0.5
            )
            axl.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 1.0),
                facecolor = (0.0, 0.0, 0.0, 0.0),
                linewidth = 0.5
            )
            axr.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 1.0),
                facecolor = (0.0, 0.0, 0.0, 0.0),
                linewidth = 0.5
            )

    # Save map as PNG ...
    fig.savefig(flightLog.replace(".csv", ".png"), bbox_inches = "tight", dpi = 300, pad_inches = 0.1)
    pyguymer3.exiftool(flightLog.replace(".csv", ".png"))
    pyguymer3.optipng(flightLog.replace(".csv", ".png"))
    matplotlib.pyplot.close("all")

    # Print out the countries that were not drawn ...
    for country in sorted(extraCountries):
        print("\"{:s}\" was not drawn.".format(country))

    # Print out the countries that have been visited ...
    for country in sorted(visited):
        print("\"{:s}\" has been visited.".format(country))
