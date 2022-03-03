import os

import numpy as np

# c1 [EUR/m], c2 [EUR/m2]
c1_default, c2_default = 212, 4464
const_coeff = {
    "DE": (349, 4213),
    "ES": (354, 4314),
    "FR": (349, 4213),
    "HR": (349, 4213),
    "IT": (349, 4213),
    "LT": (71, 3262),
    "HU": (349, 4213),
    "NL": (549, 3370),
    "SE": (439, 4073),
    "UK": (549, 2236),
    "AT": (349, 4213),
    "BE": (549, 3370),
    "BG": (349, 4213),
    "CY": (540, 2087),
    "CZ": (349, 4213),
    "DK": (439, 4073),
    "EE": (71, 3262),
    "FI": (439, 4073),
    "EL": (540, 2087),
    "IE": (549, 2236),
    "LV": (71, 3262),
    "LU": (549, 3370),
    "MT": (540, 2087),
    "PL": (349, 4213),
    "PT": (354, 4314),
    "RO": (349, 4213),
    "SK": (349, 4213),
    "SI": (540, 2087),
}


class Param:
    def __init__(self, params):
        self.scenario = params["scenario"]
        self.country = params["country"]
        self.distribution_grid_cost_ceiling = params["distribution_grid_cost_ceiling"]
        # pixel threshold may not be changed. 20 is the correct value.
        self.pix_threshold = params["pix_threshold"]
        self.DH_threshold = params["DH_threshold"]
        self.total_investment_annuity = np.inf
        self.investment_increasing_factor = 1
        self.start_year = params["start_year"]
        if params["start_year"] > params["last_year"]:
            params["last_year"] = params["start_year"] + 1
        self.last_year = params["last_year"]
        self.st_dh_connection_rate = params["st_dh_connection_rate"]
        self.end_dh_connection_rate = params["end_dh_connection_rate"]
        self.depreciation_period = params["depreciation_period"]
        self.interest = params["interest"]
        if params["use_default_cost_factors"] is True:
            self.c1, self.c2 = const_coeff[self.country]
        else:
            self.c1 = params["c1"]
            self.c2 = params["c2"]
        self.case = (
            str(self.st_dh_connection_rate)
            + "_"
            + str(self.end_dh_connection_rate)
            + "_"
            + str(self.distribution_grid_cost_ceiling)
        )


class Out_File_Path(Param):
    def __init__(self, directory, in_raster_hdm, in_raster_gfa, params):
        super().__init__(params)
        self.inRasterHDM_st = in_raster_hdm
        self.inRasterHDM_end = in_raster_hdm
        self.inRasterGFA_st = in_raster_gfa
        self.inRasterGFA_end = in_raster_gfa
        self.dstDir = os.path.join(directory, self.case)
        self.maxDHdem = os.path.join(self.dstDir, "max_dh_demand_in_year.tif")
        self.supplied_heat_during_investment_period = os.path.join(
            self.dstDir, "total_supplied_heat_during_investment_period.tif"
        )
        self.invest_Euro = os.path.join(self.dstDir, "absolute_investment_Euro.tif")
        # self.hdm_cut_last_year = os.path.join(self.dstDir, 'hdm_cut_last_year.tif')
        self.total_dist_pipe_length = os.path.join(
            self.dstDir, "total_distribution_pipe_length.tif"
        )
        self.total_serv_pipe_length = os.path.join(
            self.dstDir, "total_service_pipe_length.tif"
        )
        self.coh_area_bool = os.path.join(self.dstDir, "coherent_areas_bool.tif")
        self.labels = os.path.join(self.dstDir, "labels.tif")
        self.inv_dist = os.path.join(self.dstDir, "specific_distribution_pipe_cost.tif")
        self.inv_service_pipe = os.path.join(
            self.dstDir, "specific_service_pipe_cost.tif"
        )
        self.inv_sum = os.path.join(self.dstDir, "specific_investment_total.tif")
        self.output_shp1 = os.path.join(self.dstDir, "tmp_shape.shp")
        self.output_shp2 = os.path.join(self.dstDir, "tmp_summary.shp")
        self.output_geojson = os.path.join(self.dstDir, "gis_summary.geojson")
        self.output_csv = os.path.join(self.dstDir, "summary.csv")
        self.logfile = os.path.join(self.dstDir, "info.log")
