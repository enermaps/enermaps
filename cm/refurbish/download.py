#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging as log

import urllib3
from BaseCM import cm_hddcdd

import refurbish as rf

logging = log.getLogger("cm-refurbish/download.py")
logging.setLevel(log.DEBUG)


def download_building_stock():
    csv_path = rf.path_building_stock()
    if not csv_path.exists():
        csv_url = "https://gitlab.com/hotmaps/building-stock/-/raw/master/data/building_stock.csv"
        http = urllib3.PoolManager()
        logging.info(
            f"Downloading building stock data\n  - from: {csv_url}\n  - to: {csv_path}"
        )
        with http.request("GET", csv_url, preload_content=False) as csv_req, open(
            csv_path, "b+w"
        ) as csv_file:
            csv_file.write(csv_req.read())
        logging.info("Done!")
    else:
        logging.info(
            f"Building stock file already exists: {csv_path}. Download SKIPPED!"
        )


def download_population():
    pop_path = rf.path_population()
    if not pop_path.exists():
        pop_url = "https://gisco-services.ec.europa.eu/distribution/v2/lau/geojson/LAU_RG_01M_2020_4326.geojson"
        http = urllib3.PoolManager()
        logging.info(
            f"Downloading population data\n  - from: {pop_url}\n  - to: {pop_path}"
        )
        with http.request("GET", pop_url, preload_content=False) as pop_req, open(
            pop_path, "b+w"
        ) as pop_file:
            pop_file.write(pop_req.read())
        logging.info("Done!")
    else:
        logging.info(f"Population file already exists: {pop_path}. Download SKIPPED!")


def download_tabula_Umean():
    tab_path = rf.path_tabula_Umean()
    if not tab_path.exists():
        tab_url = "https://gitlab.inf.unibz.it/URS/enermaps/tabula/-/raw/main/data/tabula-umean.csv"
        http = urllib3.PoolManager()
        logging.info(
            f"Downloading tabula data\n  - from: {tab_url}\n  - to: {tab_path}"
        )
        with http.request("GET", tab_url, preload_content=False) as tab_req, open(
            tab_path, "b+w"
        ) as tab_file:
            tab_file.write(tab_req.read())
        logging.info("Done!")
    else:
        logging.info(f"Tabula file already exists: {tab_path}. Download SKIPPED!")


def download_datasets():
    """Download the data sets required by the CM."""
    # download HDDs and CDDs data set if not already available
    # breakpoint()
    cm_hddcdd.download_data()

    # download the datasets required by the refurbish CM.
    bstk_path = rf.path_building_stock()
    print(f"{bstk_path}: {bstk_path.exists()}")
    download_building_stock()
    print(f"{bstk_path}: {bstk_path.exists()}")

    pop_path = rf.path_population()
    print(f"{pop_path}: {pop_path.exists()}")
    download_population()
    print(f"{bstk_path}: {bstk_path.exists()}")

    tab_path = rf.path_tabula_Umean()
    print(f"{tab_path}: {tab_path.exists()}")
    download_tabula_Umean()
    print(f"{bstk_path}: {bstk_path.exists()}")


if __name__ == "__main__":
    download_datasets()
