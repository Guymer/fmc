#!/usr/bin/env python3

# Import modules ...
import cartopy

# Find file containing all the country shapes ...
shape_file = cartopy.io.shapereader.natural_earth(
    resolution = "10m",
      category = "cultural",
          name = "airports"
)

# Loop over records ...
for record in cartopy.io.shapereader.Reader(shape_file).records():
    # Loop over attributes ...
    for attribute in record.attributes:
        # Check if any of them contain the first part of "Stansted Airport" ...
        if "stan" in str(record.attributes[attribute]).lower():
            # Print out the IATA code and the matching attribute ...
            print(record.attributes["iata_code"], record.attributes[attribute])
