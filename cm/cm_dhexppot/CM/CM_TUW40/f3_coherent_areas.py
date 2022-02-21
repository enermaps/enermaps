import os
import sys

import numpy as np
from scipy.ndimage import measurements

import CM.CM_TUW4.district_heating_potential as DHP
from CM.CM_TUW0.rem_mk_dir import rm_file
from CM.CM_TUW1.read_raster import raster_array
from CM.CM_TUW4.polygonize import polygonize
from CM.CM_TUW19 import run_cm as CM19

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def distribuition_costs(P, OFP, struct=np.ones((3, 3))):
    """
    For the explanation of input parameters, refer to the calculation_module.py!

    Here, three criteria should be checked in order to define the coherent areas.
        1. The total investment in distribution grid may not exceed the available capital for investment multiplied by
        a factor greater than one. If we get more regions, after clustering, they will be filtered out and only
        profitable clusters will remain. The factor should not be too big otherwise, it adds to the complexity of
        solving the problem, without additional benefit.
        2. The specific distribution grid cost [EUR/MWh], may not exceed the input cost ceiling.

    In this code, the highest priority is given to the coherent areas with highest demand.
    """

    increased_total_investment = (
        P.investment_increasing_factor * P.total_investment_annuity
    )
    invest_Euro_arr = raster_array(OFP.invest_Euro)
    supplied_heat_horizon = raster_array(OFP.supplied_heat_during_investment_period)
    maxDHdem = raster_array(OFP.maxDHdem)
    reg_filter = supplied_heat_horizon.astype(bool).astype("int8")
    # hdm_cut_last_year_arr, geo_transform = raster_array(OFP.hdm_cut_last_year, return_gt=True)
    hdm_cut_last_year_arr, geo_transform = raster_array(
        OFP.inRasterHDM_end, return_gt=True
    )
    hdm_copy = hdm_cut_last_year_arr.copy()
    hdm_cut_last_year_arr *= reg_filter
    rast_origin = geo_transform[0], geo_transform[3]
    coh_areas = np.zeros_like(supplied_heat_horizon, "int8")
    flag = True
    DH_threshold_MWh = P.DH_threshold * 1000
    pix_threshold = P.pix_threshold
    pix_threshold_st = P.pix_threshold
    while flag:
        # calculate coherent regions with given thresholds
        # DH_Regions: boolean array showing DH regions

        DH_Regions, hdm_dh_region_cut, gt, total_heat_demand = DHP.DHReg(
            hdm_cut_last_year_arr, pix_threshold, P.DH_threshold, rast_origin
        )
        # multiplication with reg_filter required to follow out_raster_maxDHdem
        # pattern and separate connection of regions with pixels that have
        # value of zero in out_raster_maxDHdem
        result = DH_Regions.astype(int)
        labels, nr_coherent = measurements.label(result, structure=struct)
        objects = measurements.find_objects(labels)
        if nr_coherent == 0:
            flag = False
            continue
        for i, obj in enumerate(objects):
            lbl_slice = labels[obj]
            tmp_lbl_pixels = lbl_slice == i + 1
            q = np.sum(supplied_heat_horizon[obj][tmp_lbl_pixels])
            q_max = np.sum(maxDHdem[obj][tmp_lbl_pixels])
            q_inv = np.sum(invest_Euro_arr[obj][tmp_lbl_pixels])
            q_spec_cost = q_inv / q

            # DH Threshold to MW
            if q_max < DH_threshold_MWh:
                hdm_cut_last_year_arr[obj][tmp_lbl_pixels] = 0
                continue
            if q_spec_cost <= P.distribution_grid_cost_ceiling:
                coh_areas[obj][tmp_lbl_pixels] = 1
                hdm_cut_last_year_arr[obj][tmp_lbl_pixels] = 0
        pix_threshold += 10
        labels = None
    labels = None
    nr_coherent = None
    print(
        "%s pixel thresholds - st: %s , end: %s"
        % (P.country, pix_threshold_st, pix_threshold)
    )
    # labels, numLabels = measurements.label(coh_areas, structure=struct)

    CM19.main(OFP.coh_area_bool, geo_transform, "int8", coh_areas)
    DHPot, labels = DHP.DHPotential(coh_areas, hdm_copy)
    CM19.main(OFP.labels, geo_transform, "int16", labels)
    print("number of labels: ", np.max(labels))
    if np.max(labels) > 0:
        polygonize(
            OFP.coh_area_bool, OFP.labels, OFP.output_shp1, OFP.output_shp2, DHPot
        )
