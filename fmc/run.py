#!/usr/bin/env python3

# Define function ...
def run(flightLog, /, *, extraCountries = None, notVisited = None, renames = None):
    # Import standard modules ...
    import csv

    # Import special modules ...
    try:
        import cartopy
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import matplotlib
        matplotlib.rcParams.update(
            {
                   "backend" : "Agg",                                           # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
                "figure.dpi" : 300,
                 "font.size" : 8,
            }
        )
        import matplotlib.pyplot
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

    # Populate default values ...
    if extraCountries is None:
        extraCountries = []
    if notVisited is None:
        notVisited = []
    if renames is None:
        renames = {}

    # **************************************************************************

    # Set the half-width of the bars on the histogram ...
    hw = 0.2

    # Create figure ...
    fg = matplotlib.pyplot.figure(figsize = (8, 12))

    # Create axes ...
    axT = fg.add_subplot(
        3,
        2,
        (1, 2),
        projection = cartopy.crs.Robinson(),
    )
    axL = pyguymer3.geo.add_top_down_axis(
        fg,
        -97.0,
        +40.0,
        2400.0e3,
        nrows = 3,
        ncols = 2,
        index = 3,
    )
    axR = pyguymer3.geo.add_top_down_axis(
        fg,
        +13.0,
        +54.0,
        2000.0e3,
        nrows = 3,
        ncols = 2,
        index = 4,
    )
    axB = fg.add_subplot(
        3,
        2,
        (5, 6),
    )

    # Configure axis (top) ...
    axT.set_global()
    pyguymer3.geo.add_map_background(axT, resolution = "large8192px")

    # Configure axis (left) ...
    pyguymer3.geo.add_map_background(axL, resolution = "large8192px")

    # Configure axis (right) ...
    pyguymer3.geo.add_map_background(axR, resolution = "large8192px")

    # Add notable lines of latitude manually (top) ...
    y1 = 66.0 + 33.0 / 60.0 + 46.2 / 3600.0                                     # [°]
    y2 = 23.0 + 26.0 / 60.0 + 13.8 / 3600.0                                     # [°]
    pyguymer3.geo.add_horizontal_gridlines(
        axT,
        locs = [-y2, -y1, 0.0, +y1, +y2],
    )

    # Add notable lines of longitude and latitude manually (left) ...
    pyguymer3.geo.add_horizontal_gridlines(
        axL,
        locs = range(-90, +100, 10),
    )
    pyguymer3.geo.add_vertical_gridlines(
        axL,
        locs = range(-180, +190, 10),
    )

    # Add notable lines of longitude and latitude manually (right) ...
    pyguymer3.geo.add_horizontal_gridlines(
        axR,
        locs = range(-90, +100, 10),
    )
    pyguymer3.geo.add_vertical_gridlines(
        axR,
        locs = range(-180, +190, 10),
    )

    # Load airport list ...
    db = load_airport_list()

    # Initialize flight dictionary, histograms and total distance ...
    flights = {}
    businessX = []
    businessY = []                                                              # [1000 km]
    pleasureX = []
    pleasureY = []                                                              # [1000 km]
    minYear = 0
    maxYear = pyguymer3.now().year
    total_dist = 0.0                                                            # [km]

    # Open flight log ...
    with open(flightLog, "rt", encoding = "utf-8") as fObj:
        # Loop over all flights ...
        for row in csv.reader(fObj):
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

            # Find the great circle ...
            circle = pyguymer3.geo.great_circle(
                lon1,
                lat1,
                lon2,
                lat2,
                npoint = 101,
            )

            # Draw the great circle ...
            axT.add_geometries(
                pyguymer3.geo.extract_lines(circle),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 1.0),
                facecolor = "none",
                linewidth = 1.0,
            )
            axL.add_geometries(
                pyguymer3.geo.extract_lines(circle),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 1.0),
                facecolor = "none",
                linewidth = 1.0,
            )
            axR.add_geometries(
                pyguymer3.geo.extract_lines(circle),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 1.0),
                facecolor = "none",
                linewidth = 1.0,
            )

            # Find countries and add them to the list if either are missing ...
            country1 = country_of_IATA(db, iata1)
            country2 = country_of_IATA(db, iata2)
            if country1 not in extraCountries:
                extraCountries.append(country1)
            if country2 not in extraCountries:
                extraCountries.append(country2)

    # Plot histograms ...
    axB.bar(businessX, businessY, width = 2.0 * hw, label = "Business")
    axB.bar(pleasureX, pleasureY, width = 2.0 * hw, label = "Pleasure")
    axB.grid()
    axB.legend(loc = "upper right")
    # axB.set_xticks(                                                             # MatPlotLib ≥ 3.5.0
    #     range(minYear, maxYear + 1),                                            # MatPlotLib ≥ 3.5.0
    #       labels = range(minYear, maxYear + 1),                                 # MatPlotLib ≥ 3.5.0
    #           ha = "right",                                                     # MatPlotLib ≥ 3.5.0
    #     rotation = 45,                                                          # MatPlotLib ≥ 3.5.0
    # )                                                                           # MatPlotLib ≥ 3.5.0
    axB.set_xticks(range(minYear, maxYear + 1))                                   # MatPlotLib < 3.5.0
    axB.set_xticklabels(                                                        # MatPlotLib < 3.5.0
        range(minYear, maxYear + 1),                                            # MatPlotLib < 3.5.0
              ha = "right",                                                     # MatPlotLib < 3.5.0
        rotation = 45,                                                          # MatPlotLib < 3.5.0
    )                                                                           # MatPlotLib < 3.5.0
    axB.set_ylabel("Distance [1000 km/year]")

    # Add annotation ...
    label = f"You have flown {total_dist:,.1f} km."
    label += f" You have flown around the Earth {total_dist / (0.001 * pyguymer3.CIRCUMFERENCE_OF_EARTH):,.1f} times."
    label += f" You have flown to the Moon {total_dist / (0.001 * pyguymer3.EARTH_MOON_DISTANCE):,.1f} times."
    axT.text(
        0.5,
        -0.02,
        label,
        horizontalalignment = "center",
                  transform = axT.transAxes,
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
            axT.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 0.25),
                facecolor = (1.0, 0.0, 0.0, 0.25),
                linewidth = 0.5,
            )
            axL.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 0.25),
                facecolor = (1.0, 0.0, 0.0, 0.25),
                linewidth = 0.5,
            )
            axR.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (1.0, 0.0, 0.0, 0.25),
                facecolor = (1.0, 0.0, 0.0, 0.25),
                linewidth = 0.5,
            )
            extraCountries.remove(neName)
        else:
            # Outline the country ...
            axT.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 0.25),
                facecolor = (0.0, 0.0, 0.0, 0.0 ),
                linewidth = 0.5,
            )
            axL.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 0.25),
                facecolor = (0.0, 0.0, 0.0, 0.0 ),
                linewidth = 0.5,
            )
            axR.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
                cartopy.crs.PlateCarree(),
                edgecolor = (0.0, 0.0, 0.0, 0.25),
                facecolor = (0.0, 0.0, 0.0, 0.0 ),
                linewidth = 0.5,
            )

    # Configure figure ...
    fg.tight_layout()

    # Save figure ...
    fg.savefig(flightLog.replace(".csv", ".png"))
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
