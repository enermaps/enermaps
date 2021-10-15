import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import rasterio
from BaseCM.cm_output import validate

GEOJSON_PROJ = "EPSG:4326"
DEFAULT_STATS = ("min", "max", "mean", "median", "count")
SCALED_STATS_PREFIX = ("min", "max", "mean", "median", "percentile_")
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

CDF_POINTS = range(0, 101)

DECIMALS = 3

CURRENT_FILE_DIR = Path(__file__).parent
TESTDATA_DIR = CURRENT_FILE_DIR / "testdata"


def scale_stat(stats: dict, factor):
    """From a list of stats, take the factor into account and
    modify the stats accordingly.
    """
    for stat_name, stat in stats.items():
        for scaled_stat_prefix in SCALED_STATS_PREFIX:
            if stat and stat_name.startswith(scaled_stat_prefix):
                stats[stat_name] = stat * factor


def compute_centroid(geojson: Dict) -> Tuple[float, float]:
    """
    Example
    >>> gj = {'features': [
    ...          {'geometry':
    ...               {'coordinates': [[[11.061588, 45.567844],
    ...                                 [11.055015, 45.563899],
    ...                                 [11.050421, 45.565349],
    ...                                 [11.040453, 45.560869],
    ...                                 [11.032734, 45.561389]]],
    ...                'type': 'Polygon'},
    ...           'id': 80284,
    ...           'properties': {'ds_id': 0,
    ...                          'dt': '',
    ...                          'fields': '',
    ...                          'id': 'IT_023038',
    ...                          'layer': '{ "type": "numerical" }',
    ...                          'start_at': '',
    ...                          'units': '{ "": null }',
    ...                          'variables': '{ "": 0 }',
    ...                          'z': ''},
    ...           'type': 'Feature'}],
    ...       'type': 'FeatureCollection'}
    >>> compute_centroid(gj)
    (11.048, 45.564)
    """
    try:
        coords = np.array(geojson["features"][0]["geometry"]["coordinates"])
    except KeyError:
        logging.error(geojson)
        raise ValueError(
            "FAILED! The provided geometry is not a correct/supported geojson format."
        )
    return tuple(np.around(coords[0].mean(0), decimals=DECIMALS))


def get_datarepodir() -> Path:
    return Path(os.environ.get("CM_HDD_CDD_REPOSITORY", TESTDATA_DIR.as_posix()))


@lru_cache(maxsize=256)
def get_datadir(
    datarepository: Path,
    sim_type: str = "historical",
    dd_type: str = "hdd",
    Tb=18.0,
    aggr_window="monthly",
    method="average",
) -> Path:
    """
    >>> get_datadir("cm/cm_hdd_cdd/testdata").as_posix()
    "cm/cm_hdd_cdd/testdata/historical/hdd/18.0/monthly/average/"
    """
    return (
        Path(datarepository) / sim_type / dd_type / f"{Tb:.1f}" / aggr_window / method
    )


@lru_cache()
def extract_by_dir(
    gdir: Path,
    lon: float,
    lat: float,
    __datasets: Dict[str, rasterio.DatasetReader] = {},
):
    res = []
    idx = []
    for gfi in gdir.iterdir():
        if gfi.name.endswith(".tif"):
            idx.append(gfi.name[:-4])
            try:
                gx = __datasets[gfi.as_posix()]
            except KeyError:
                gx = rasterio.open(gfi)
                __datasets[gfi.as_posix()] = gx
            yp, xp = gx.index(lon, lat)
            val = gx.read()[0][yp, xp]
            logging.info(
                f"{gfi.name}@{lon:.{DECIMALS}f},{lat:.{DECIMALS}f}: {yp}, {xp} => {val}"
            )
            res.append(val)
    sr = pd.Series(np.array(res), index=idx, name=f"yp={yp},xp={xp}")
    sr.sort_index(inplace=True)
    return sr


def dd_my_group(sr: pd.Series) -> pd.Series:
    isplit = sr.index.str.split("_")
    years = [yr for yr, _ in isplit]
    mnths = [mnth for _, mnth in isplit]
    yrgrp = sr.groupby(years)
    mngrp = sr.groupby(mnths)
    return mngrp, yrgrp


def hdd_cdd_stats(
    geojson: Dict,
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
    * the total annual HDD & CDD for the baseline and the future year
      with confidence interval;
    * the total monthly HDD & CDD for the baseline and the future year
      with confidence interval;

    Key Performance Indicator​s (KPIs)
    =================================
    The main KPIs provide by the function are:
    * percentage variation of HDD respect to the current scenario​;
    * percentage variation of CDD respect to the current scenario​;
    * reduction of the heating season length​
    * extension of the cooling season length
    * number of tropical days
    """
    # select the right layer and return the results
    # start = time()
    msg = (
        f"    » ref. year: {refyear},"
        f" crp: {rcp}, Tbh: {t_base_h:.1f}, Tbc: {t_base_c:.1f}"
    )
    logging.info(msg)
    # Compute the centroid of the geometry selected by the user
    print(f"CENTROID: {compute_centroid(geojson)}")
    lon, lat = compute_centroid(geojson)
    # Query the file-directory-netcdf structure for all the pixels involved
    hdd_path = get_datadir(
        datarepository=get_datarepodir(),
        sim_type=rcp,
        dd_type="hdd",
        Tb=t_base_h,
        aggr_window="monthly",
        method="average",
    )
    avg_hdds = extract_by_dir(gdir=hdd_path, lon=lon, lat=lat)
    cdd_path = get_datadir(
        datarepository=get_datarepodir(),
        sim_type=rcp,
        dd_type="cdd",
        Tb=t_base_c,
        aggr_window="monthly",
        method="average",
    )
    avg_cdds = extract_by_dir(gdir=cdd_path, lon=lon, lat=lat)
    # end = time()
    # extract the min, max, mean with their confidence intervals
    # prepare monthly and yearly graphs
    ret = dict()
    ret["graphs"] = {}

    ret["graphs"]["Monthly HDDs"] = {}
    ret["graphs"]["Monthly HDDs"]["type"] = "line"
    ret["graphs"]["Monthly HDDs"]["values"] = avg_hdds.tolist()

    ret["graphs"]["Monthly CDDs"] = {}
    ret["graphs"]["Monthly CDDs"]["type"] = "line"
    ret["graphs"]["Monthly CDDs"]["values"] = avg_cdds.tolist()

    ret["geofiles"] = {}

    # TODO: extract stats for yearly values and not monthly
    ret["values"] = {
        f"{var} {stats}": value
        for var, st in zip(["HDDs", "CDDs"], [avg_hdds.describe(), avg_cdds.describe()])
        for stats, value in st.items()
    }

    # extract the main KPIs
    # logging.info(f"We took {end - start!s} to query the data repository")

    res = validate(ret)
    # logging.info(f"Result is {res}")
    return res
