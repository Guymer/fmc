def calc_vertical_gridlines(xloc, ext):
    xlocs = []
    ylocs = []
    for yloc in range(int(round(ext[2])), int(round(ext[3])) + 1):
        xlocs.append(xloc)
        ylocs.append(yloc)
    return xlocs, ylocs