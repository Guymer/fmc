# -*- coding: utf-8 -*-

def calc_horizontal_gridlines(yloc, ext):
    xlocs = []
    ylocs = []
    for xloc in xrange(int(round(ext[0])), int(round(ext[1])) + 1):
        xlocs.append(xloc)
        ylocs.append(yloc)
    return xlocs, ylocs
