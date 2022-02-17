#!/usr/bin/env python3
import logging as log
import os
import sys
import tarfile
from functools import lru_cache
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import pyproj
import rasterio
import urllib3

logging = log.getLogger("cm-hdd_cdd")
logging.setLevel(log.DEBUG)

DECIMALS = 3
CURRENT_FILE_DIR = Path(__file__).parent
TESTDATA_DIR = CURRENT_FILE_DIR / "testdata" / "hddcddrepo"


def download_data():
    # export CM_HDD_CDD_REPOSITORY=/tmp/hddcddrepo
    # export INPUT_DATA_DIR=/tmp
    repo = Path(os.environ["CM_HDD_CDD_REPOSITORY"])
    print(f"data repository => {repo}")
    os.makedirs(repo.as_posix(), exist_ok=True)

    hist = repo / "historical"
    if hist.exists():
        print(
            f"The directory {repo} already exists, the dataset is not going to be"
            " downloaded."
        )
    else:
        print("Downloading the HDDs and CDDs dataset")
        url = "https://gitlab.inf.unibz.it/URS/enermaps/hdd-cdd/-/archive/main/hdd-cdd-main.tar.gz"
        zpath = repo / "hdd-cdd-main.tar.gz"
        http = urllib3.PoolManager()
        with http.request("GET", url, preload_content=False) as req, open(
            zpath, "b+w"
        ) as zdata:
            zdata.write(req.read())
        print(f"Extracting {zpath}")
        with tarfile.open(zpath) as zfile:
            zfile.extractall(repo)
        os.remove(zpath)
        # wget = sub.Popen(
        #     [
        #         "wget",
        #         "-O",
        #         f"{repo}/hdd-cdd-main.tar.gz",
        #         "https://gitlab.inf.unibz.it/URS/enermaps/hdd-cdd/-/archive/main/hdd-cdd-main.tar.gz",
        #     ]
        # )
        # if wget.wait():
        #     print("Not able to download the data sets")
        #     sys.exit(1)
        # extr = sub.Popen(["tar", "-xf", f"{repo}/hdd-cdd-main.tar.gz", "-C", f"{repo}"])
        # if extr.returncode:
        #     print("Not able to extract the data sets")
        #     sys.exit(1)
        # os.remove(f"{repo}/hdd-cdd-main.tar.gz")

    print("done!")
    sys.exit(0)


def compute_centroid(geo) -> Tuple[float, float]:
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
    >>> import geopandas as gpd
    >>> geo = gpd.GeoDataFrame.from_features(
    ...     gj["features"], crs="EPSG:4326"
    ... ).geometry
    >>> compute_centroid(geo)
    (11.048, 45.564)
    """
    # logging.warning(geo)
    try:
        coords = np.array(geo.to_crs("EPSG:3035").centroid.to_crs("EPSG:4326")[0])
    except KeyError:
        logging.error(geo)
        raise ValueError(
            "FAILED! The provided geometry is not a correct/supported geojson format."
        )
    return tuple(np.around(coords, decimals=DECIMALS))


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


def reproj(
    src_x: float, src_y: float, src_crs: str = "EPSG:4326", dst_crs: str = "EPSG:3035"
) -> Tuple[float, float]:
    trans = pyproj.Transformer.from_crs(src_crs, dst_crs)
    cy, cx = trans.transform(src_x, src_y)
    return (cx, cy)


@lru_cache()
def extract_by_dir(
    gdir: Path,
    lon: float,
    lat: float,
    refyear: int = None,
    refmonth: int = None,
    __datasets: Dict[str, rasterio.DatasetReader] = {},
):
    res = []
    idx = []
    # check inputs
    if refyear is not None and (refyear < 1950 or refyear > 2100):
        raise ValueError(
            f"Reference year must be 1950 <= refyear <=2100, instead is: {refyear}"
        )
    refyear = "*" if refyear is None else f"{refyear}"
    if refmonth is not None and (refmonth < 1 or refmonth > 12):
        raise ValueError(
            f"Reference month must be 1 <= refmonth <=12, instead is: {refmonth}"
        )
    refmonth = "*" if refmonth is None else f"{refmonth:02d}"

    # define the file pattern to match
    pattern = f"{refyear}_{refmonth}.tif"

    # TODO: convert lat, lon to EPSG:3035 coords
    # cx, cy = reproj(lat, lon)
    cx, cy = reproj(src_x=lat, src_y=lon, src_crs="EPSG:4326", dst_crs="EPSG:3035")
    for gfi in gdir.iterdir():
        if gfi.match(pattern):
            idx.append(gfi.name[:-4].replace("_", "-"))
            try:
                gx = __datasets[gfi.as_posix()]
            except KeyError:
                gx = rasterio.open(gfi)
                __datasets[gfi.as_posix()] = gx
            yp, xp = gx.index(cx, cy)
            if yp < 0 or xp < 0:
                raise ValueError(
                    f"Negative row|col index, row_index={yp}, col_index={xp}"
                    f"@{lon:.{DECIMALS}f}({cx:.{DECIMALS}f}),{lat:.{DECIMALS}f}({cy:.{DECIMALS}f})"
                )
            val = gx.read()[0][yp, xp]
            logging.info(
                f"{gfi.name}@{lon:.{DECIMALS}f}({cx:.{DECIMALS}f}),{lat:.{DECIMALS}f}({cy:.{DECIMALS}f}):"
                f" {yp}, {xp} => {val}"
            )
            res.append(val)
    sr = pd.Series(np.array(res), index=idx, name=f"yp={yp},xp={xp}")
    sr.sort_index(inplace=True)
    return sr
