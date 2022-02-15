# -*- coding: utf-8 -*-
"""
Created on July 6 2017

@author: fallahnejad@eeg.tuwien.ac.at
"""
import os
import sys
import time
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW9.bottom_up_hdm import zonStat_selectedArea as zs
from CM.CM_TUW9.specific_demand import specific_demand
from CM.CM_TUW9.shp2csv import shp2csv
from CM.CM_TUW9.update_building_layer import update_building_lyr as update
''' This module calls other calculation modules for the BUHDM'''
verbose = False


def main(process_bool, inputValues):
    (eu_shp, spec_demand_csv, UsefulDemandRasterPath,
     UsefulDemandRaster, inShapefile, outCSV, outShapefile,
     heatDensityRaster, gfa_density_raster, population) = inputValues
    # Process 1: creates a specific demand raster layer. The country names in
    # csv should be similar to the ones in the shapefile.
    if process_bool[0]:
        start = time.time()
        specific_demand(eu_shp, spec_demand_csv, UsefulDemandRasterPath)
        if verbose:
            print('Process 1 took: %0.2f seconds' % (time.time() - start))
    # Process 2: creates a standard csv file from the input shapefile
    if process_bool[1]:
        start = time.time()
        shp2csv(inShapefile, UsefulDemandRaster, outCSV)
        if verbose:
            print('Process 2 took: %0.2f seconds' % (time.time() - start))
    # Process 3: updates and creates a new shapefile based on the standard csv
    if process_bool[2]:
        start = time.time()
        inputCSV = outCSV
        update(inputCSV, inShapefile, outShapefile)
        if verbose:
            print('Process 3 took: %0.2f seconds' % (time.time() - start))
    # Process 4: generates a heat density map
    inputCSV = outCSV
    start = time.time()
    outputs = zs(inputCSV, heatDensityRaster, gfa_density_raster, population)
    """
    Outputs are:
        Absolute heat demand: [GWh\a]
        Mean heat demand per capita: [kWh\n]
        Mean heat demand per heated surface (ave. specific demand): [kWh/m2]
    """
    if verbose:
        print('Process 4 took: %0.2f seconds' % (time.time() - start))
    return outputs, outCSV, outShapefile, heatDensityRaster


if __name__ == "__main__":
    start = time.time()
    process1 = False
    process2 = True
    process3 = True
    population = 1000
    project_path = path + os.sep + 'AD/data_warehouse'
    eu_shp = project_path + os.sep + "AT.shp"
    spec_demand_csv = project_path + os.sep + "useful demand.csv"
    UsefulDemandRasterPath = project_path
    ResidentialUsefulDemand = project_path + os.sep + "ResidentialUseful" \
                                                      "Demand_AT.tif"
    ServiceUsefulDemand = project_path + os.sep + "ServiceUsefulDemand_AT.tif"
    UsefulDemandRaster = [ResidentialUsefulDemand, ServiceUsefulDemand]
    inShapefile = project_path + os.sep + "Sample_OSM_Building_Lyr.shp"
    output_dir = path + os.sep + 'Outputs'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    outCSV = output_dir + os.sep + "CM9_building_strd_info.csv"
    outShapefile = output_dir + os.sep + "CM9_updated_building_" \
                                         "footprint_AT.shp"
    heatDensityRaster = output_dir + os.sep + "CM9_Heat_Density_Map.tif"
    process_bool = (process1, process2, process3)
    inputValues = (eu_shp, spec_demand_csv, UsefulDemandRasterPath,
                   UsefulDemandRaster, inShapefile, outCSV, outShapefile,
                   heatDensityRaster, population)
    output = main(process_bool, inputValues)
    print('The whole process took %0.2f seconds' % (time.time() - start))
    print(output)
