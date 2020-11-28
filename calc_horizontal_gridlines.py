def calc_horizontal_gridlines(yloc, ext):
    xlocs = []
    ylocs = []
    for xloc in range(int(round(ext[0])), int(round(ext[1])) + 1):
        xlocs.append(xloc)
        ylocs.append(yloc)
    return xlocs, ylocs