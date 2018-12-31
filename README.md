# Flight Map Creator (FMC)

This module contains all the functions required to create a map of the world with all of your flights overlaid and all of the countries that you have visited shaded in. It also contains an [example input file](example.csv) so that you know what is required to make it work too. The format for a line is `departure airport IATA code`, `arrival airport IATA code`, `year of flight`, `Business`/`Pleasure`. Whilst the flights do not have to be in order in the CSV file the first flight *does* have to have occurred in the first year.

## Usage

FMC can be run very easily, below is an example (also found in [example.py](example.py)).

```python
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
    ],
    renames = {
        "Czech Republic" : "Czechia",
        "United States" : "United States of America"
    }
)
```

You must pass it the path to a CSV file containing all of the flights that you have taken. Additionally, you can optionally pass it a list of other countries that you have visited but that you might not have flown to (`extraCountries`). FMC uses two different databases of countries behind the scenes and (very annoyingly) they use different names for some countries. If any of these are ones that you have visited then you can correct FMC's behaviour by explicitly providing a dictionary of countries to be renamed (`renames`).

## Example Output

FMC will create a PNG in the directory of the CSV file. Below is the result for the included file [example.csv](example.csv).

![FMC output for the example](example.png)

## Dependencies

FMC requires the following Python modules to be installed and available in your `PYTHONPATH`.

* [cartopy](https://pypi.python.org/pypi/Cartopy)
* [matplotlib](https://pypi.python.org/pypi/matplotlib)
* [pyguymer](https://github.com/Guymer/PyGuymer)

FMC uses some [Natural Earth](http://www.naturalearthdata.com/) resources via the [Cartopy](http://scitools.org.uk/cartopy/) module. If they do not exist on your system then Cartopy will download them for you in the background. Consequently, a working internet connection may be required the first time you run FMC.
