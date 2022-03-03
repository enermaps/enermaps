import logging
import os
import sys
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)
from tempfile import TemporaryDirectory
import numpy as np
import pandas as pd
#from BaseCM.cm_output import validate
from CM.CM_TUW0.rem_mk_dir import rm_dir, rm_mk_dir  # , copy_dir
from CM.CM_TUW40.f1_main_call import main
from CM.CM_TUW40.f4_results_summary import summary
from initialize import Out_File_Path, Param
from tools import settings
from tools.areas import get_areas
from tools.geofile import clip_raster, get_projection, write_raster
from tools.response import get_response


'''
def createLegend(
    preds: np.array,
    name: str = "Potential district heating areas",
    unit: str = "-",
    nb_class: int = 2,
) -> dict:
    """Prepare a legend dict in HotMaps format"""
    nb_class = min([nb_class, preds[~np.isnan(preds)].shape[0] - 1])
    if nb_class > 2:
        color_scale = cm.get_cmap("plasma", nb_class).colors
        color_scale[:, :-1] *= 255

        breaks = jenkspy.jenks_breaks(preds[~np.isnan(preds)], nb_class=nb_class)

        legend = {"name": name, "type": "custom", "symbology": []}
        for i in range(len(breaks) - 1):
            legend["symbology"].append(
                {
                    "red": float(color_scale[i, 0]),
                    "green": float(color_scale[i, 1]),
                    "blue": float(color_scale[i, 2]),
                    "opacity": float(color_scale[i, 3]),
                    "value": float(breaks[i]),
                    "label": "≥ {} {}".format(int(round(breaks[i], 0)), unit),
                }
            )
    else:
        legend = {}
        print("No legend was created.", flush=True)
    return legend
'''

def logfile(P, OFP):
    logging_text = "\n\n"
    P_attr_dict = vars(P)
    col_width = 5 + max(len(key) for key in P_attr_dict.keys())
    for key in P_attr_dict.keys():
        logging_text = logging_text + "".join(
            key.ljust(col_width) + str(P_attr_dict[key]).ljust(col_width) + "\n"
        )
    with open(OFP.logfile, "w") as f:
        f.write(logging_text)


def unify_excels(output_directory):
    init_df = True
    for root, dirs, files in os.walk(output_directory):
        for file in files:
            if "summary.csv" == file:
                f = os.path.join(root, "summary.csv")
                tmp_df = pd.read_csv(f)
                if init_df:
                    df = tmp_df.copy()
                    init_df = False
                else:
                    df = df.append(tmp_df, ignore_index=True)
    out_xlsx = os.path.join(output_directory, "summary_all.xlsx")
    df.to_excel(out_xlsx, index=False)


def res_calculation(region: dict, in_raster_hdm_large, in_raster_gfa_large, params):
    P = Param(params)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with TemporaryDirectory(dir=current_dir) as directory:
        if not os.path.isdir(directory) or not os.path.exists(directory):
            raise NotADirectoryError(f"Directory not created : {directory}")
        else:
            logging.info(msg=f"Dir created : {directory}")
        in_raster_hdm = os.path.join(directory, "hdm.tif")
        in_raster_gfa = os.path.join(directory, "gfa.tif")
        clip_raster(in_raster_hdm_large, region, in_raster_hdm)
        clip_raster(in_raster_gfa_large, region, in_raster_gfa)
        OFP = Out_File_Path(directory, P, in_raster_hdm, in_raster_gfa)
        # P.warnings()
        rm_mk_dir(OFP.dstDir)
        logfile(P, OFP)
        main(P, OFP)
        result_dict = summary(P, OFP)
        #####################################################################
        # Dict return response
        ret = dict()
        ret["graphs"] = []
        # ret["geofiles"] = {"file": OFP.coh_area_bool}
        # ret["legend"] = createLegend(np.arange(2))
        ret["geofiles"] = {}
        ret["values"] = {
            "Starting connection rate (%)": P.st_dh_connection_rate,
           "End connection rate (%)": P.end_dh_connection_rate,
           "Grid cost ceiling (EUR/MWh)": P.distribution_grid_cost_ceiling,
            "Start year - Heat demand in DH areas (GWh)": float(np.sum(
                result_dict["demand_st [GWh]"]
            )),
            "End year - Heat demand in areas (GWh)": float(np.sum(
                result_dict["demand_end [GWh]"]
            )),
            "Start year - Heat coverage by DH areas (GWh)": float(np.sum(
                result_dict["dhPot_%s [GWh]" % P.start_year]
            )),
            "End year - Heat coverage by DH areas (GWh)": float(np.sum(
                result_dict["dhPot_%s [GWh]" % P.last_year]
            )),
            "Total supplied heat by DH over the investment period (TWh)": float(np.sum(
                result_dict["supplied_heat_over_investment_period [TWh]"]
            )),
            "Average DH grid cost in DH areas (EUR/MWh)": float(np.round_(
                (
                    np.sum(result_dict["gridCost [MEUR]"])
                    / np.sum(result_dict["supplied_heat_over_investment_period [TWh]"])
                ),
                2,
            )),
            "Total DH distribution grid length (km)": float(np.sum(
                result_dict["trench_len_dist [km]"]
            )),
            "Total DH service pipe length (km)": float(np.sum(
                result_dict["trench_len_dist [km]"]
            )),
        }
        # logging.info("We took {!s} to deploy the model".format(pred_done - start))
    #validate(ret)
    return ret
