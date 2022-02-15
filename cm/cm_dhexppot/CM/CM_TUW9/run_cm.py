'''
Created on Jul 26, 2017

@author: simulant
'''
import os
import sys
import time
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
import CM.CM_TUW9.main_block as mb


def main(process_bool, inputValues):
    outputs = mb.main(process_bool, inputValues)
    return outputs

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
    main(process_bool, inputValues)
    print('The whole process took %0.2f seconds' % (time.time() - start))
