# -*- coding: utf-8 -*-
import os
import sys

import numpy as np
import pandas as pd

import CM.CM_TUW19.run_cm as CM19

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def zonStat_selectedArea(
    inputCSV, hdm_outRasterPath, gfa_outRasterPath, population=0, resolution=100
):
    """
    This function calculates the sum of demand within a pixels with given
    resolution. The pixel will also overlay to the standard fishnet used for
    the hotmaps toolbox since the multiplying factor matches to distances from
    the origin of the standard fishnet. The code assumes a resolution of
    100x100 m for the output.
    annual building demand must be in kWh/a
    output heat density map raster is in MWh/ha
    """
    if isinstance(inputCSV, pd.DataFrame):
        ifile = inputCSV
    else:
        if not os.path.isfile(inputCSV):
            raise
        ifile = pd.read_csv(inputCSV)
    demand = ifile["demand"].values
    GFA = ifile["GFA"].values
    if np.sum(GFA):
        GFA_valid = True
    else:
        GFA_valid = False
    X = ifile["X_3035"].values
    Y = ifile["Y_3035"].values
    x0 = resolution * np.floor(np.min(X) / resolution).astype(int)
    y0 = resolution * np.ceil(np.max(Y) / resolution).astype(int)
    rasterOrigin = (x0, y0)
    xIndex = np.floor((X - x0) / resolution).astype(int)
    yIndex = np.floor((y0 - Y) / resolution).astype(int)
    xWidth = np.max(xIndex) - np.min(xIndex) + 1
    yWidth = np.max(yIndex) - np.min(yIndex) + 1
    index = xIndex + xWidth * yIndex
    # The number of rows of "index" and "demand" must be equal.
    sortedData = np.asarray(sorted(zip(index, demand), key=lambda x: x[0]))
    sortedData_GFA = np.asarray(sorted(zip(index, GFA), key=lambda x: x[0]))
    unique, counts = np.unique(index, return_counts=True)
    end = np.cumsum(counts)
    st = np.concatenate((np.zeros((1)), end[0 : end.size - 1]))
    # xIndex and yIndex start from 0. So they should be added by 1
    sumDem = np.zeros((np.max(xIndex) + 1) * (np.max(yIndex) + 1))
    item_location = 0
    if GFA_valid:
        sumGFA = np.zeros_like(sumDem)
        for item in unique:
            # sum of demand for each index
            startIndex = int(st[item_location])
            endIndex = int(end[item_location])
            sumDem[item] = np.sum(sortedData[startIndex:endIndex, 1])
            sumGFA[item] = np.sum(sortedData_GFA[startIndex:endIndex, 1])
            item_location += 1
    else:
        for item in unique:
            # sum of demand for each index
            startIndex = int(st[item_location])
            endIndex = int(end[item_location])
            sumDem[item] = np.sum(sortedData[startIndex:endIndex, 1])
            item_location += 1
    """
    xWidth and yWidth in the following refer to columns and rows,
    respectively and should not wrongly be considered as coordination!
    """

    sumDem = sumDem.reshape((yWidth, xWidth))
    geo_transform = [rasterOrigin[0], resolution, 0, rasterOrigin[1], 0, -resolution]
    CM19.main(hdm_outRasterPath, geo_transform, str(sumDem.dtype), sumDem)
    abs_heat_demand = np.sum(demand)
    if GFA_valid:
        # gross floor area density map
        sumGFA = sumGFA.reshape((yWidth, xWidth))
        CM19.main(gfa_outRasterPath, geo_transform, str(sumGFA.dtype), sumGFA)
        mean_spec_demand = abs_heat_demand / np.sum(GFA)
    else:
        mean_spec_demand = np.nan
    if population:
        mean_dem_perCapita = abs_heat_demand / float(population)
    else:
        mean_dem_perCapita = np.nan
    #     print("Absolute heat demand: %0.1f GWh\a"
    #           "Mean heat demand per capita: %0.2f kWh\n"
    #           "Mean heat demand per heated surface (ave. specific demand): %0.2f"
    #           " kWh/m2"
    #           % (abs_heat_demand*10**(-6), mean_dem_perCapita, mean_spec_demand))
    return (abs_heat_demand * 10 ** (-6), mean_dem_perCapita, mean_spec_demand)
