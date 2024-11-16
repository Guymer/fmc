#!/usr/bin/env python3

# Define function ...
def run(
    flightLog,
    /,
    *,
               dat = "airports.dat",
             debug = __debug__,
    extraCountries = None,
         flightMap = None,
          leftDist = 2392.2e3,          # These default values come from my own
           leftLat = +39.411078,        # personal flight log.
           leftLon = -97.871822,
           maxYear = None,
           minYear = None,
        notVisited = None,
          optimize = True,
           renames = None,
         rightDist = 2345.0e3,          # These default values come from my own
          rightLat = +49.879310,        # personal flight log.
          rightLon =  +3.172021,
             strip = True,
           timeout = 60.0,
):
    """Make a PNG map from a CSV file

    Parameters
    ----------
    flightLog : str
        the CSV of your flights
    dat : str, optional
        the OpenFlights airport database CSV to load (at time of writing, only
        "airports.dat" and "airports-extended.dat" will work)
    debug : bool, optional
        print debug messages
    extraCountries : list of str, optional
        a list of extra countries that you have visited but which you have not
        flown to (e.g., you took a train)
    flightMap : str, optional
        the PNG map
    leftDist : float, optional
        the field-of-view around the left-hand sub-map central point (in metres)
    leftLat : float, optional
        the latitude of the central point of the left-hand sub-map (in degrees)
    leftLon : float, optional
        the longitude of the central point of the left-hand sub-map (in degrees)
    maxYear : int, optional
        the maximum year to use for the survey
    minyear : int, optional
        the minimum year to use for the survey
    notVisited : list of str, optional
        a list of countries which you have flown to but not visited (e.g., you
        just transferred planes)
    optimize : bool, optional
        optimize the PNG map
    renames : dict, optional
        a mapping from OpenFlights country names to Natural Earth country names
    rightDist : float, optional
        the field-of-view around the right-hand sub-map central point (in metres)
    rightLat : float, optional
        the latitude of the central point of the right-hand sub-map (in degrees)
    rightLon : float, optional
        the longitude of the central point of the right-hand sub-map (in degrees)
    strip : bool, optional
        strip metadata from PNG map too
    timeout : float, optional
        the timeout for any requests/subprocess calls (in seconds)

    Notes
    -----
    Copyright 2016 Thomas Guymer [1]_

    References
    ----------
    .. [1] FMC, https://github.com/Guymer/fmc
    """

    # Import standard modules ...
    import csv
    import json
    import os

    # Import special modules ...
    try:
        import cartopy
        cartopy.config.update(
            {
                "cache_dir" : os.path.expanduser("~/.local/share/cartopy_cache"),
            }
        )
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import matplotlib
        matplotlib.rcParams.update(
            {
                       "backend" : "Agg",                                       # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
                    "figure.dpi" : 300,
                "figure.figsize" : (9.6, 7.2),                                  # NOTE: See https://github.com/Guymer/misc/blob/main/README.md#matplotlib-figure-sizes
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

    # Populate default values ...
    if extraCountries is None:
        extraCountries = []
    if flightMap is None:
        flightMap = f'{flightLog.removesuffix(".csv")}.png'
    if maxYear is None:
        maxYear = pyguymer3.now().year
    if notVisited is None:
        notVisited = []
    if renames is None:
        renames = {}

    # **************************************************************************

    # Set the half-width of the bars on the histogram ...
    hw = 0.2

    # Create figure ...
    # NOTE: I would like to use (4.8, 7.2) so as to be consistent with all my
    #       other figures (see linked 4K discussion above), however, the result
    #       is very poor due to the too wide, single line, summary label/string.
    #       The result gets even worse when ".tight_layout()" is called.
    fg = matplotlib.pyplot.figure(figsize = (2 * 4.8, 2 * 7.2))

    # Create axes ...
    axT = pyguymer3.geo.add_axis(
        fg,
        debug = debug,
        index = (1, 2),
        ncols = 2,
        nrows = 3,
    )
    axL = pyguymer3.geo.add_axis(
        fg,
        debug = debug,
         dist = leftDist,
        index = 3,
          lat = leftLat,
          lon = leftLon,
        ncols = 2,
        nrows = 3,
    )
    axR = pyguymer3.geo.add_axis(
        fg,
        debug = debug,
         dist = rightDist,
        index = 4,
          lat = rightLat,
          lon = rightLon,
        ncols = 2,
        nrows = 3,
    )
    axB = fg.add_subplot(
        3,
        2,
        (5, 6),
    )

    # Configure axis (top) ...
    pyguymer3.geo.add_map_background(
        axT,
             debug = debug,
        resolution = "large8192px",
    )

    # Configure axis (left) ...
    pyguymer3.geo.add_map_background(
        axL,
             debug = debug,
        resolution = "large8192px",
    )

    # Configure axis (right) ...
    pyguymer3.geo.add_map_background(
        axR,
             debug = debug,
        resolution = "large8192px",
    )

    # Load airport list ...
    with open(f"{os.path.dirname(__file__)}/db.json", "rt", encoding = "utf-8") as fObj:
        airports = json.load(fObj)

    # Initialize flight dictionary, histograms and total distance ...
    flights = {}
    businessX = []
    businessY = []                                                              # [1000 km]
    pleasureX = []
    pleasureY = []                                                              # [1000 km]
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
                if debug:
                    print(f"DEBUG: A flight does not have valid IATA codes (\"{iata1}\" and \"{iata2}\").")
                continue

            # Check if this is the first line ...
            if len(businessX) == 0:
                # Set the minimum year (if required)...
                if minYear is None:
                    minYear = int(row[2][0:4])

                # Loop over the full range of years ...
                for year in range(minYear, maxYear + 1):
                    # NOTE: This is a bit of a hack, I should really use NumPy
                    #       but I do not want to bring in another dependency
                    #       that people may not have.
                    businessX.append(year - hw)
                    businessY.append(0.0)                                       # [1000 km]
                    pleasureX.append(year + hw)
                    pleasureY.append(0.0)                                       # [1000 km]

            # Extract the year that this flight started in and skip if it is out
            # of scope ...
            year = int(row[2][0:4])
            if year < minYear:
                if debug:
                    print(f"DEBUG: A flight between {iata1} and {iata2} took place in {year:d}, which was before {minYear:d}.")
                continue
            if year > maxYear:
                if debug:
                    print(f"DEBUG: A flight between {iata1} and {iata2} took place in {year:d}, which was after {maxYear:d}.")
                continue

            # Find coordinates for this flight ...
            lon1, lat1 = coordinates_of_IATA(airports, iata1)                   # [°], [°]
            lon2, lat2 = coordinates_of_IATA(airports, iata2)                   # [°], [°]
            if debug:
                print(f"INFO: You have flown between {iata1}, which is at ({lat1:+10.6f}°,{lon1:+11.6f}°), and {iata2}, which is at ({lat2:+10.6f}°,{lon2:+11.6f}°).")
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

            # Add it's distance to the histogram (if it is one of the two
            # recognised fields) ...
            match row[3].lower():
                case "business":
                    businessY[businessX.index(year - hw)] += 0.001 * dist       # [1000 km]
                case "pleasure":
                    pleasureY[pleasureX.index(year + hw)] += 0.001 * dist       # [1000 km]
                case _:
                    pass

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
                  debug = debug,
                maxdist = 12.0 * 1852.0,
                 npoint = None,
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
            country1 = country_of_IATA(airports, iata1)
            country2 = country_of_IATA(airports, iata2)
            if country1 not in extraCountries:
                extraCountries.append(country1)
            if country2 not in extraCountries:
                extraCountries.append(country2)

    # Plot histograms ...
    axB.bar(
        businessX,
        businessY,
        label = "Business",
        width = 2.0 * hw,
    )
    axB.bar(
        pleasureX,
        pleasureY,
        label = "Pleasure",
        width = 2.0 * hw,
    )
    axB.legend(loc = "upper right")
    # axB.set_xticks(                                                             # MatPlotLib ≥ 3.5.0
    #     range(minYear, maxYear + 1),                                            # MatPlotLib ≥ 3.5.0
    #       labels = range(minYear, maxYear + 1),                                 # MatPlotLib ≥ 3.5.0
    #           ha = "right",                                                     # MatPlotLib ≥ 3.5.0
    #     rotation = 45,                                                          # MatPlotLib ≥ 3.5.0
    # )                                                                           # MatPlotLib ≥ 3.5.0
    axB.set_xticks(range(minYear, maxYear + 1))                                 # MatPlotLib < 3.5.0
    axB.set_xticklabels(                                                        # MatPlotLib < 3.5.0
        range(minYear, maxYear + 1),                                            # MatPlotLib < 3.5.0
              ha = "right",                                                     # MatPlotLib < 3.5.0
        rotation = 45,                                                          # MatPlotLib < 3.5.0
    )                                                                           # MatPlotLib < 3.5.0
    axB.set_ylabel("Distance [1000 km/year]")
    axB.yaxis.grid(True)

    # Loop over years ...
    for i in range(minYear, maxYear + 1, 2):
        # Configure axis ...
        # NOTE: As of 13/Aug/2023, the default "zorder" of the bars is 1.0 and
        #       the default "zorder" of the vspans is 1.0.
        axB.axvspan(
            i - 0.5,
            i + 0.5,
                alpha = 0.25,
            facecolor = "grey",
               zorder = 0.0,
        )

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
    fg.savefig(flightMap)
    matplotlib.pyplot.close(fg)

    # Optimize PNG (if required) ...
    if optimize:
        pyguymer3.image.optimize_image(
            flightMap,
              debug = debug,
              strip = strip,
            timeout = timeout,
        )

    # Print out the countries that were not drawn ...
    for country in sorted(extraCountries):
        print(f"\"{country}\" was not drawn.")

    # Print out the countries that have been visited ...
    for country in sorted(visited):
        print(f"\"{country}\" has been visited.")
