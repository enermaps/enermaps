# import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Dict

import geopandas as gpd
import pandas as pd
from BaseCM.cm_output import validate
from shapely import geometry
from shapely.geometry import shape

CURRENT_FILE_DIR = Path(__file__).parent

BS2TABULA = {
    "Appartment blocks": ("AB",),
    "Education": (),
    "Health": (),
    "Hotels and Restaurants": (),
    "Multifamily houses": ("MFH",),
    "Offices": (),
    "Other non-residential buildings": (),
    "Single family - Terraced houses": ("SFH", "TH"),
    "Total": (),
    "Trade": (),
}


def path_building_stock() -> Path:
    return CURRENT_FILE_DIR / "data" / os.environ["BUILSTK"]


@lru_cache()
def get_building_stock() -> pd.DataFrame:
    """Return building_stock dataframe"""
    bs = pd.read_csv(path_building_stock(), sep="|", index_col=0)
    # fix label adding a space
    bs.loc[
        bs["btype"] == "Single family- Terraced houses", "btype"
    ] = "Single family - Terraced houses"
    return bs


def path_population() -> Path:
    return CURRENT_FILE_DIR / "data" / os.environ["POPGJSN"]


@lru_cache()
def get_population() -> gpd.GeoDataFrame:
    """Return building_stock dataframe"""
    return gpd.read_file(path_population(), crs="EPSG:4326")


@lru_cache()
def get_population_centroids() -> gpd.GeoDataFrame:
    """Return building_stock dataframe"""
    return get_population().centroid


def path_tabula_Umean() -> Path:
    return CURRENT_FILE_DIR / "data" / "all-umean.xlsx"


@lru_cache()
def get_tabula_Umean() -> pd.DataFrame:
    """Return building_stock dataframe"""
    tab = pd.read_excel(path_tabula_Umean(), index_col=0)
    # harmonize building types
    tab["bstype"] = ""
    for label, vals in BS2TABULA.items():
        for val in vals:
            idx = tab["btype"] == val
            tab.loc[idx, "bstype"] = label
    return tab


def download_dataset():
    """Download the data set required by the CM."""
    # check if the file already exists in the local directory
    # if file are not present, then download the latest version
    raise NotImplementedError


def get_laus(
    user_selection: geometry.Polygon, lau: gpd.GeoDataFrame, centroids: gpd.GeoDataFrame
):
    # check which LAU2 contains the user selection centroid
    # if user is selecting using the LAU2
    ucentroid = user_selection.centroid
    laus0 = lau.loc[lau.contains(ucentroid), :]
    # check which LAU2 centroids are contained in the user selection
    # if the user is selecting using NUTS{1|2|3}
    laus1 = lau.loc[centroids.within(user_selection), :]
    if len(laus1) == 0:
        # user is selecting using LAU2
        laus = laus0
    else:
        laus = laus1
    return laus


def ref_rate(
    geojson: Dict,
    bstype: str,
    start_year: int,
    end_year: int,
    perc_basic: float,
    perc_advance: float,
    refyear: int = 2050,
    rcp: str = "4.5",
    t_base_h: float = 18.0,
    t_base_c: float = 22.0,
):
    """
    The `ref_rate` returns a set of graphs and KPI based on the refurbish
    rate selected by the user for a specific:
    * sector (residential, industrial, tertiary);
    * epoch of construction (1950-1960, 1961-1970, etc.);
    * building typology (single family house, multi family house, building block, etc.)
    """
    # transform dict to shapely geometry
    user_selection = shape(geojson["features"][0]["geometry"])
    # get population data
    pop = get_population()
    # get population centroids
    centroids = get_population_centroids()
    # get building stock
    bstk = get_building_stock()
    # get tabula values
    tab = get_tabula_Umean()

    # select the LAUs selected by the user
    laus = get_laus(user_selection, pop, centroids)

    # get and check the country code
    cntr_code = laus["CNTR_CODE"].drop_duplicates()
    if len(cntr_code) > 1:
        # TODO: handle selection with multiple country involved
        raise ValueError(f"Multiple countries selection ({cntr_code}) not supported")

    # extract the total population numbers
    cntr_code = cntr_code.iloc[0]
    cntr_pop = pop.loc[pop["CNTR_CODE"] == cntr_code, "POP_2020"].sum()
    sel_pop = laus["POP_2020"].sum()

    hbsel = bstk.loc[
        (
            (bstk["country_code"] == cntr_code.lower())
            & (bstk["btype"] == bstype)
            & (bstk["bage"] == "1970 - 1979")
            & (bstk["unit"] == "Mm²")
            & (bstk["type"] == "Heated area [Mm²]")
        )
    ]
    cbsel = bstk.loc[
        (
            (bstk["country_code"] == cntr_code.lower())
            & (bstk["btype"] == bstype)
            & (bstk["bage"] == "1970 - 1979")
            & (bstk["unit"] == "Mm²")
            & (bstk["type"] == "Cooled area [Mm²]")
        )
    ]

    if len(hbsel) > 1:
        raise ValueError
    if len(cbsel) > 1:
        raise ValueError

    heating_m2 = hbsel["value"].iloc[0] * 1_000_000.0 / cntr_pop * sel_pop
    cooling_m2 = cbsel["value"].iloc[0] * 1_000_000.0 / cntr_pop * sel_pop

    tsel = (
        (tab["country"] == cntr_code.upper())
        & (tab["country"] == cntr_code.upper())
        # & ((tab["start"].astype(int) >= start_year)
        # | (tab["end"].astype(int) <= end_year))
        & (tab["bstype"] == bstype)
    )

    stab = tab.loc[tsel, :]
    syears = (
        stab["start"].drop_duplicates().astype(int).sort_values().reset_index(drop=True)
    )
    eyears = (
        stab["end"].drop_duplicates().astype(int).sort_values().reset_index(drop=True)
    )
    start_valid = syears[syears.loc[syears > start_year].index[0] - 1]
    end_valid = eyears[eyears.loc[eyears < end_year].index[-1] + 1]

    staby = stab.loc[
        (
            (tab["start"].astype(int) >= start_valid)
            & (tab["end"].astype(int) <= end_valid)
        ),
    ]

    grp = staby.groupby(by=["epoch", "bstype", "rtype"])
    char = grp[["actual_floor_value1", "U mean [W/(m²K)]", "Tot. surface [m²]"]].mean()

    denominator = len(char)
    h_m2 = heating_m2 / denominator
    c_m2 = cooling_m2 / denominator

    h_nbuildings = (h_m2 / char["actual_floor_value1"]).round(0)
    c_nbuildings = (c_m2 / char["actual_floor_value1"]).round(0)

    # TODO: mutiply by HDDs and CDDs
    h_enrg = (
        h_nbuildings * char["U mean [W/(m²K)]"] * char["Tot. surface [m²]"]
    ).unstack()
    c_enrg = (
        c_nbuildings * char["U mean [W/(m²K)]"] * char["Tot. surface [m²]"]
    ).unstack()

    h_savings_ur = h_enrg["cs"] - h_enrg["ur"]
    h_savings_ar = h_enrg["cs"] - h_enrg["ar"]

    c_savings_ur = c_enrg["cs"] - c_enrg["ur"]
    c_savings_ar = c_enrg["cs"] - c_enrg["ar"]

    # prepare the CM output
    ret = dict()
    ret["graphs"] = {}
    ret["geofiles"] = {}

    ret["values"] = {
        "Savings on {} | {} | {} | {}".format(
            demand_type,
            refurbish_type,
            epoch,
            building_type,
        ): value
        for demand_type, data, refurbish_type in zip(
            ["heating", "heating", "cooling", "cooling"],
            [h_savings_ur, h_savings_ar, c_savings_ur, c_savings_ar],
            [
                "usual refurbish",
                "advance refurbish",
                "advance refurbish",
                "usual refurbish",
            ],
        )
        for (epoch, building_type), value in data.items()
    }

    res = validate(ret)
    return res
