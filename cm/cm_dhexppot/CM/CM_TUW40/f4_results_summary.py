import os
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
from osgeo import ogr
from scipy.ndimage import measurements

from CM.CM_TUW1.read_raster import raster_array as RA

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def measure_sum(arr, labels, index, factor=1):
    if factor == 1:
        return np.round_(measurements.sum(arr, labels, index), 2)
    else:
        return np.round_(factor * measurements.sum(arr, labels, index), 2)


def summary(P, OFP, struct=np.ones((3, 3))):
    labels_org = RA(OFP.labels)
    labels_arr = labels_org.astype(bool).astype(int)
    zero_elements = np.where(labels_arr == 0)
    maxDHdem_arr = RA(OFP.maxDHdem)
    supplied_heat_horizon = RA(OFP.supplied_heat_during_investment_period)
    invest_Euro_arr = RA(OFP.invest_Euro)
    hdm_cut_st_arr = RA(OFP.inRasterHDM_st)
    hdm_cut_end_arr = RA(OFP.inRasterHDM_end)
    gfa_cut_st_arr = RA(OFP.inRasterGFA_st)
    gfa_cut_end_arr = RA(OFP.inRasterGFA_end)
    total_dist_pipe_length = RA(OFP.total_dist_pipe_length)
    total_serv_pipe_length = RA(OFP.total_serv_pipe_length)

    supplied_heat_horizon[zero_elements] = 0
    maxDHdem_arr[zero_elements] = 0
    invest_Euro_arr[zero_elements] = 0
    hdm_cut_st_arr[zero_elements] = 0
    hdm_cut_end_arr[zero_elements] = 0
    gfa_cut_st_arr[zero_elements] = 0
    gfa_cut_end_arr[zero_elements] = 0
    total_dist_pipe_length[zero_elements] = 0
    total_serv_pipe_length[zero_elements] = 0

    # labels, nr_coherent = measurements.label(total_pipe_length_arr.astype(bool).astype(int), structure=struct)
    nr_coherent = int(np.max(labels_org))
    index, fp = np.unique(labels_org, return_counts=True)
    # exclude zero
    index = index[1:].astype(int)
    fp = fp[1:]

    floorArea_st = measure_sum(gfa_cut_st_arr, labels_org, index)
    floorArea_end = measure_sum(gfa_cut_end_arr, labels_org, index)
    demand_st = measure_sum(hdm_cut_st_arr, labels_org, index)
    demand_end = measure_sum(hdm_cut_end_arr, labels_org, index)
    q_max = measure_sum(maxDHdem_arr, labels_org, index)
    q = measure_sum(supplied_heat_horizon, labels_org, index)
    q_inv = measure_sum(invest_Euro_arr, labels_org, index)
    # pipe is in m/m2 and needs factor 1e4 for ha
    tot_dist_pipe_len = measure_sum(total_dist_pipe_length, labels_org, index, 1e4)
    tot_serv_pipe_len = measure_sum(total_serv_pipe_length, labels_org, index, 1e4)
    q_spec_cost1 = np.round_(q_inv / q, 2)
    q_spec_cost2 = np.round_(q_inv / tot_dist_pipe_len, 2)
    nr_rows = len(index)
    d = {
        "country": np.array([P.country] * nr_rows),
        "st_conn_rate [%]": np.array([P.st_dh_connection_rate] * nr_rows),
        "end_conn_rate [%]": np.array([P.end_dh_connection_rate] * nr_rows),
        "grid_cost_ceiling [EUR/MWh]": np.array(
            [P.distribution_grid_cost_ceiling] * nr_rows
        ),
        "Label": index,
        "demand_st [GWh]": demand_st / 1e3,
        "demand_end [GWh]": demand_end / 1e3,
        "gfa_st [ha]": floorArea_st / 1e4,
        "gfa_end [ha]": floorArea_end / 1e4,
        "footprint_dh_area [ha]": fp,
        "dhPot_%s [GWh]" % P.start_year: demand_st * P.st_dh_connection_rate * 1e-3,
        "dhPot_%s [GWh]" % P.last_year: demand_end * P.end_dh_connection_rate * 1e-3,
        "maxDHdem [GWh]": q_max * 1e-3,
        "supplied_heat_over_investment_period [TWh]": np.round_(q * 1e-6, 3),
        "gridCost [MEUR]": q_inv / 1e6,
        "spCostEn [EUR/MWh]": q_spec_cost1,
        "spCostMet (wo. serv. pipe) [EUR/m]": q_spec_cost2,
        "trench_len_dist [km]": tot_dist_pipe_len / 1e3,
        "trench_len_serv [km]": tot_serv_pipe_len / 1e3,
    }
    df = pd.DataFrame(data=d)
    df.to_csv(OFP.output_csv, index=False)

    if nr_coherent > 0:
        gdf = gpd.read_file(OFP.output_shp2)
        gdf = gdf.drop(columns=["Dem_DhArea", "fillColor", "color", "opacity"])
        gdf["Label"] = gdf["Label"].values.astype(int)
        # gdf2 = gdf.merge(df, on='Label', how='left', lsuffix='l_')
        gdf2 = gdf.merge(df, on="Label")
        gdf = None
        gdf2.to_file(OFP.output_geojson, driver="GeoJSON")
        out_driver = ogr.GetDriverByName("ESRI Shapefile")
        if os.path.exists(OFP.output_shp2):
            out_driver.DeleteDataSource(OFP.output_shp2)
    return d
