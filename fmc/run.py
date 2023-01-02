def run(kwArgCheck = None, extraCountries = [], flightLog = "/this/path/does/not/exist", notVisited = [], renames = {}):
    # Import standard modules ...
    import csv

    # Import special modules ...
    try:
        import cartopy
        import cartopy.crs
        import cartopy.io
        import cartopy.io.shapereader
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import matplotlib
        matplotlib.use("Agg")                                                   # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
        import matplotlib.image
        import matplotlib.pyplot
        matplotlib.pyplot.rcParams.update({"font.size" : 8})
    except:
        raise Exception("\"matplotlib\" is not installed; run \"pip install --user matplotlib\"") from None

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.geo
        import pyguymer3.image
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # Import sub-functions ...
    from .coordinates_of_IATA import coordinates_of_IATA
    from .country_of_IATA import country_of_IATA
    from .load_airport_list import load_airport_list

    # Check keyword arguments ...
    if kwArgCheck is not None:
        print(f"WARNING: \"{__name__}\" has been called with an extra positional argument")

    # Set extents of the three sub-plots ...
    extt = [
        -180.0, # left
         180.0, # right
         -90.0, # bottom
          90.0, # top
    ]                                                                           # [°]
    extl = [
        -120.0, # left
         -70.0, # right
          17.0, # bottom
          55.0, # top
    ]                                                                           # [°]
    extr = [
         -10.0, # left
          40.0, # right
          33.0, # bottom
          71.0, # top
    ]                                                                           # [°]

    # Set the half-width of the bars on the histogram ...
    hw = 0.2

    # Create plot and make it pretty ...
    fg = matplotlib.pyplot.figure(figsize = (8, 12), dpi = 300)
    gs = fg.add_gridspec(29, 20)
    axt = fg.add_subplot(gs[ 0:10,  0:20], projection = cartopy.crs.Robinson())
    axl = fg.add_subplot(gs[10:19,  0:10], projection = cartopy.crs.Orthographic(central_longitude = 0.5 * (extl[0] + extl[1]), central_latitude = 0.5 * (extl[2] + extl[3])))
    axr = fg.add_subplot(gs[10:19, 10:20], projection = cartopy.crs.Orthographic(central_longitude = 0.5 * (extr[0] + extr[1]), central_latitude = 0.5 * (extr[2] + extr[3])))
    axb = fg.add_subplot(gs[19:29,  0:20])
    axt.set_global()
    axl.set_extent(extl)
    axr.set_extent(extr)
    pyguymer3.geo.add_map_background(axt, resolution = "large8192px")
    pyguymer3.geo.add_map_background(axl, resolution = "large8192px")
    pyguymer3.geo.add_map_background(axr, resolution = "large8192px")
    axt.coastlines(resolution = "10m", color = "black", linewidth = 0.1)
    axl.coastlines(resolution = "10m", color = "black", linewidth = 0.1)
    axr.coastlines(resolution = "10m", color = "black", linewidth = 0.1)

    # Add notable lines of latitude manually (top) ...
    y1 = 66.0 + 33.0 / 60.0 + 46.2 / 3600.0                                     # [°]
    y2 = 23.0 + 26.0 / 60.0 + 13.8 / 3600.0                                     # [°]
    pyguymer3.geo.add_horizontal_gridlines(axt, extt, locs = [-y2, -y1, 0.0, +y1, +y2])

    # Add notable lines of longitude and latitude manually (left) ...
    pyguymer3.geo.add_horizontal_gridlines(axl, extl, locs = range(-90, +100, 10))
    pyguymer3.geo.add_vertical_gridlines(axl, extl, locs = range(-180, +190, 10))

    # Add notable lines of longitude and latitude manually (right) ...
    pyguymer3.geo.add_horizontal_gridlines(axr, extr, locs = range(-90, +100, 10))
    pyguymer3.geo.add_vertical_gridlines(axr, extr, locs = range(-180, +190, 10))

    # Load airport list ...
    db = load_airport_list()

    # Initialize flight dictionary, histograms and total distance ...
    flights = {}
    businessX = []
    businessY = []                                                              # [1000 km]
    pleasureX = []
    pleasureY = []                                                              # [1000 km]
    minYear = 0
    total_dist = 0.0                                                            # [km]

    # Open flight log ...
    with open(flightLog, "rt", encoding = "utf-8") as fobj:
        # Loop over all flights ...
        for row in csv.reader(fobj):
            # Extract IATA codes for this flight ...
            iata1 = row[0]
            iata2 = row[1]

            # Skip this flight if the codes are not what I expect ...
            if len(iata1) != 3 or len(iata2) != 3:
                continue

            # Check if this is the first line ...
            if len(businessX) == 0:
                # Set the minimum year ...
                minYear = int(row[2][0:4])

                # Loop over the full range of years ...
                for year in range(minYear, pyguymer3.now().year + 1):
                    # NOTE: This is a bit of a hack, I should really use NumPy
                    #       but I do not want to bring in another dependency
                    #       that people may not have.
                    businessX.append(year - hw)
                    businessY.append(0.0)                                       # [1000 km]
                    pleasureX.append(year + hw)
                    pleasureY.append(0.0)                                       # [1000 km]

            # Find coordinates for this flight ...
            lon1, lat1 = coordinates_of_IATA(db, iata1)                         # [°], [°]
            lon2, lat2 = coordinates_of_IATA(db, iata2)                         # [°], [°]
            dist, _, _ = pyguymer3.geo.calc_dist_between_two_locs(
                lon1,
                lat1,
                lon2,
                lat2,
            )                                                                   # [m]

            # Convert m to km ...
            dist *= 0.001                                                       # [km]

            # Add it's distance to the total ...
            total_dist += dist                                                  # [km]

            # Add it's distance to the histogram ...
            if row[3].lower() == "business":
                businessY[businessX.index(int(row[2][0:4]) - hw)] += 0.001 * dist   # [1000 km]
            elif row[3].lower() == "pleasure":
                pleasureY[pleasureX.index(int(row[2][0:4]) + hw)] += 0.001 * dist   # [1000 km]

            # Create flight name and skip this flight if it has already been
            # drawn ...
            if iata1 < iata2:
                flight = f"{iata1}2{iata2}"
            else:
                flight = f"{iata2}2{iata1}"
            if flight in flights:
                continue
            flights[flight] = True

            # Draw the great circle ...
            axt.plot(
                [lon1, lon2],
                [lat1, lat2],
                    color = "red",
                linewidth = 1.0,
                transform = cartopy.crs.Geodetic(),
            )
            axl.plot(
                [lon1, lon2],
                [lat1, lat2],
                    color = "red",
                linewidth = 1.0,
                transform = cartopy.crs.Geodetic(),
            )
            axr.plot(
                [lon1, lon2],
                [lat1, lat2],
                    color = "red",
                linewidth = 1.0,
                transform = cartopy.crs.Geodetic(),
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
    axb.grid()
    axb.legend()
    axb.set_xticks(range(minYear, pyguymer3.now().year + 1))
    axb.set_ylabel("Distance [1000 km/year]")

    # Add annotation ...
    label = f"You have flown {total_dist:,.1f} km. You have flown around the Earth {total_dist / 40030.2:,.1f} times. You have flown to the Moon {total_dist / 384402.0:,.1f} times."
    axt.text(
        0.5,
        -0.02,
        label,
                   fontsize = 6,
        horizontalalignment = "center",
                  transform = axt.transAxes,
          verticalalignment = "center",
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
    sfile = cartopy.io.shapereader.natural_earth(
          category = "cultural",
              name = "admin_0_countries",
        resolution = "10m",
    )

    # Initialize visited list ...
    visited = []

    # Loop over records ...
    for record in cartopy.io.shapereader.Reader(sfile).records():
        # Create short-hand ...
        neName = pyguymer3.geo.getRecordAttribute(record, "NAME")

        # Check if this country is in the list ...
        if neName in extraCountries and neName not in notVisited:
            # Append country name to visited list ...
            visited.append(neName)

            # Fill the country in and remove it from the list ...
            # NOTE: Removing them from the list enables us to print out the ones
            #       that where not found later on.
            axt.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 0.25),
                facecolor = (1.0, 0.0, 0.0, 0.25),
                linewidth = 0.5,
            )
            axl.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 0.25),
                facecolor = (1.0, 0.0, 0.0, 0.25),
                linewidth = 0.5,
            )
            axr.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 0.25),
                facecolor = (1.0, 0.0, 0.0, 0.25),
                linewidth = 0.5,
            )
            extraCountries.remove(neName)
        else:
            # Outline the country ...
            axt.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 0.25),
                facecolor = (0.0, 0.0, 0.0, 0.0 ),
                linewidth = 0.5,
            )
            axl.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 0.25),
                facecolor = (0.0, 0.0, 0.0, 0.0 ),
                linewidth = 0.5,
            )
            axr.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 0.25),
                facecolor = (0.0, 0.0, 0.0, 0.0 ),
                linewidth = 0.5,
            )

    # Configure figure ...
    fg.tight_layout()

    # Save figure ...
    fg.savefig(
        flightLog.replace(".csv", ".png"),
               dpi = 300,
        pad_inches = 0.1,
    )
    matplotlib.pyplot.close(fg)

    # Optimize PNG ...
    pyguymer3.image.optimize_image(
        flightLog.replace(".csv", ".png"),
        strip = True,
    )

    # Print out the countries that were not drawn ...
    for country in sorted(extraCountries):
        print(f"\"{country}\" was not drawn.")

    # Print out the countries that have been visited ...
    for country in sorted(visited):
        print(f"\"{country}\" has been visited.")
