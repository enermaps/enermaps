import logging
import os
from tempfile import TemporaryDirectory

import pandas as pd
from BaseCM.cm_output import validate

from CM.CM_TUW0.rem_mk_dir import rm_mk_dir
from CM.CM_TUW1.read_raster import raster_array as RA
from CM.CM_TUW40.f1_main_call import main
from CM.CM_TUW40.f4_results_summary import summary
from initialize import Out_File_Path, Param
from tools.geofile import clip_raster
from tools.response import get_response


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

        response = get_response(
            RA(OFP.inv_sum, dType="float32"),
            P,
            result_dict,
            OFP.inv_sum,
        )
        """
        #####################################################################
        # Dict return response
        ret = dict()
        ret["graphs"] = []
        ret["geofiles"] = {"areas": OFP.inv_sum}
        ret["legend"] = get_legend(RA(OFP.inv_sum, dType="float32"))
        print(ret["legend"])

        ret["values"] = {
            "Starting connection rate (%)": 100 * P.st_dh_connection_rate,
           "End connection rate (%)": 100 * P.end_dh_connection_rate,
           "Grid cost ceiling (EUR/MWh)": P.distribution_grid_cost_ceiling,
            "Start year - Heat demand in DH areas (GWh)": round(float(np.sum(
                result_dict["demand_st [GWh]"]
            )), 1),
            "End year - Heat demand in areas (GWh)": round(float(np.sum(
                result_dict["demand_end [GWh]"]
            )), 1),
            "Start year - Heat coverage by DH areas (GWh)": round(float(np.sum(
                result_dict["dhPot_%s [GWh]" % P.start_year]
            )), 1),
            "End year - Heat coverage by DH areas (GWh)": round(float(np.sum(
                result_dict["dhPot_%s [GWh]" % P.last_year]
            )), 1),
            "Total supplied heat by DH over the investment period (TWh)": round(float(np.sum(
                result_dict["supplied_heat_over_investment_period [TWh]"]
            )), 1),
            "Average DH grid cost in DH areas (EUR/MWh)": float(np.round_(
                (
                    np.sum(result_dict["gridCost [MEUR]"])
                    / np.sum(result_dict["supplied_heat_over_investment_period [TWh]"])
                ),
                2,
            )),
            "Total DH distribution grid length (km)": round(float(np.sum(
                result_dict["trench_len_dist [km]"]
            )), 1),
            "Total DH service pipe length (km)": round(float(np.sum(
                result_dict["trench_len_dist [km]"]
            )), 1),
        }
        """
        # logging.info("We took {!s} to deploy the model".format(pred_done - start))
    validate(response)
    return response
