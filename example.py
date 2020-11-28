#!/usr/bin/env python3

# Import modules ...
import fmc

# Run function ...
fmc.run(
    flightLog = "example.csv",
    extraCountries = [
        "Denmark",
        "Germany",
        "Ireland",
        "Myanmar",
        "Nepal",
        "Netherlands",
        "Russia",
        "Switzerland",
    ],
    notVisited = [
        "Hong Kong",
        "Singapore",
    ],
    renames = {
        "Czech Republic" : "Czechia",
        "United States" : "United States of America",
    }
)
