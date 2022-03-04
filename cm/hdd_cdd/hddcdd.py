#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging as log

from BaseCM import cm_hddcdd
from BaseCM.cm_output import validate

logging = log.getLogger("cm-hdd_cdd")
logging.setLevel(log.DEBUG)


def hdd_cdd_stats(
    geo,
    refyear: int = 2050,
    rcp: str = "4.5",
    t_base_h: float = 18.0,
    t_base_c: float = 22.0,
):
    """The `hdd_cdd_stats` returns a set of graphs and KPI extracted by the HDD and CDD
    layers computed starting from the EURO CORDEX ensamble simulations.

    Graphs​
    ======
    This funtion return the following graphs:
    * the total annual HDD & CDD for the baseline and the future year;
    * the total monthly HDD & CDD for the baseline and the future year;

    Key Performance Indicator​s (KPIs)
    =================================
    The main KPIs provide by the function are:
    * HDDs yearly statistics​;
    * CDDs yearly statistics;
    """

    msg = (
        f"    » ref. year: {refyear},"
        f" crp: {rcp}, Tbh: {t_base_h:.1f}, Tbc: {t_base_c:.1f}"
    )
    logging.info(msg)
    # Compute the centroid of the geometry selected by the user
    lon, lat = cm_hddcdd.compute_centroid(geo)
    logging.info(f"CENTROID: lon: {lon}, lat: {lat}")
    # Query the file-directory-netcdf structure for all the pixels involved
    hdd_path = cm_hddcdd.get_datadir(
        datarepository=cm_hddcdd.get_datarepodir(),
        sim_type=rcp,
        dd_type="hdd",
        Tb=t_base_h,
    )
    # extract, cast to int from uint8 and transform * 10
    avg_hdds = cm_hddcdd.extract_by_dir(gdir=hdd_path, lon=lon, lat=lat)
    hdds = avg_hdds.astype(int) * 10

    cdd_path = cm_hddcdd.get_datadir(
        datarepository=cm_hddcdd.get_datarepodir(),
        sim_type=rcp,
        dd_type="cdd",
        Tb=t_base_c,
    )
    # extract, cast to int from uint8 and transform * 10
    avg_cdds = cm_hddcdd.extract_by_dir(gdir=cdd_path, lon=lon, lat=lat)
    cdds = avg_cdds.astype(int) * 10

    # add yearly stats
    yhdds = hdds.groupby(hdds.index.str[:4]).sum()
    ycdds = cdds.groupby(cdds.index.str[:4]).sum()
    graphs = []
    values = []

    if len(yhdds):
        yr_hdd = {}
        yr_hdd["Yearly HDDs"] = {}
        yr_hdd["Yearly HDDs"]["type"] = "bar"
        yr_hdd["Yearly HDDs"]["values"] = list(yhdds.items())
        graphs.append(yr_hdd)
        values.extend(
            [
                (f"Yearly HDDs {stat}", value)
                for stat, value in yhdds.describe().astype(str).items()
            ]
        )
    else:
        values.append(("Yearly HDDs: Dataset not available", 0))

    if len(ycdds):
        yr_cdd = {}
        yr_cdd["Yearly CDDs"] = {}
        yr_cdd["Yearly CDDs"]["type"] = "bar"
        yr_cdd["Yearly CDDs"]["values"] = list(ycdds.items())
        graphs.append(yr_cdd)
        values.extend(
            [
                (f"Yearly CDDs {stat}", value)
                for stat, value in ycdds.describe().astype(str).items()
            ]
        )
    else:
        values.append(("Yearly CDDs: Dataset not available", 0))

    # prepare monthly and yearly graphs
    if len(hdds):
        mon_hdd = {}
        mon_hdd["Monthly HDDs"] = {}
        mon_hdd["Monthly HDDs"]["type"] = "line"
        mon_hdd["Monthly HDDs"]["values"] = list(hdds.items())
        graphs.append(mon_hdd)

    if len(cdds):
        mon_cdd = {}
        mon_cdd["Monthly CDDs"] = {}
        mon_cdd["Monthly CDDs"]["type"] = "line"
        mon_cdd["Monthly CDDs"]["values"] = list(cdds.items())
        graphs.append(mon_cdd)

    ret = dict()
    ret["graphs"] = graphs
    ret["geofiles"] = {}

    ret["values"] = {key: value for key, value in values}

    validate(ret)
    logging.info(f"Result is:\n{ret}")
    return ret
