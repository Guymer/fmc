#!/usr/bin/env python2

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
        "Switzerland"
    ],
    renames = {
        "Czech Republic" : "Czechia",
        "United States" : "United States of America"
    }
)
