import os
import time
import sys
import numpy as np
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW4.polygonize import polygonize
from CM.CM_TUW0.rem_mk_dir import rm_mk_dir, rm_file
import CM.CM_TUW4.district_heating_potential as DHP
import CM.CM_TUW19.run_cm as CM19


def main(heat_density_map, pix_threshold, DH_threshold, output_raster1,
         output_raster2, output_shp1, output_shp2, in_orig=None,
         only_return_areas=False):
    # DH_Regions: boolean array showing DH regions
    DH_Regions, hdm_dh_region_cut, geo_transform, total_heat_demand = DHP.DHReg(heat_density_map,
                                                                                 pix_threshold,
                                                                                 DH_threshold,
                                                                                 in_orig)
    if only_return_areas:
        geo_transform = None
        return DH_Regions
    DHPot, labels = DHP.DHPotential(DH_Regions, heat_density_map)
    total_potential = np.around(np.sum(DHPot),2)
    total_heat_demand = np.around(total_heat_demand, 2)
    if total_potential == 0:
        dh_area_flag = False
    else:
        dh_area_flag = True

    symbol_vals_str = []
    if dh_area_flag:
        CM19.main(output_raster1, geo_transform, 'int8', DH_Regions)
        temp_raster = os.path.dirname(output_raster2) + '/temp.tif'
        CM19.main(temp_raster, geo_transform, 'int32', labels)
        symbol_vals_str = polygonize(output_raster1, temp_raster,
                                     output_shp1, output_shp2, DHPot)
        rm_file(temp_raster, temp_raster[:-4] + '.tfw')
        CM19.main(output_raster2, geo_transform, 'float32', hdm_dh_region_cut)

    return total_potential, total_heat_demand, symbol_vals_str
