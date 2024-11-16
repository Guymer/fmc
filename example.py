#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import modules ...
    import fmc

    # Run function ...
    fmc.run(
        "example.csv",
                 debug = False,
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
                                        #               airport database → shape database
                                                               "Türkiye" : "Turkey",
            "United Kingdom of Great Britain and Northern Ireland (the)" : "United Kingdom",
                                        "United States of America (the)" : "United States of America",
                                                              "Viet Nam" : "Vietnam",
        }
    )
