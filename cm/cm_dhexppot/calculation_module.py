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


def res_calculation(region: dict, in_raster_hdm_large, in_raster_gfa_large, params, task, not_test_mode: bool = True):
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
        OFP = Out_File_Path(directory, in_raster_hdm, in_raster_gfa, params)
        rm_mk_dir(OFP.dstDir)
        logfile(P, OFP)
        main(P, OFP)
        result_dict = summary(P, OFP)
        if not_test_mode:
            if os.path.isfile(OFP.inv_sum):
                with open(OFP.inv_sum, mode="rb") as raster_fd:
                    task.post_raster(raster_name="result.tif", raster_fd=raster_fd)
            else:
                raise FileExistsError(f"File doest not exist : {OFP.inv_sum}")
        response = get_response(
            RA(OFP.inv_sum, dType="float32"),
            P,
            result_dict,
            OFP.inv_sum,
        )
    validate(response)
    return response
