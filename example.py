#!/usr/bin/env python

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
    ]
)
