import logging as log
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Tuple

import geopandas as gpd
import pandas as pd
from BaseCM import cm_hddcdd
from BaseCM.cm_output import validate
from shapely import geometry

logging = log.getLogger("cm-refurbish")
logging.setLevel(log.DEBUG)

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

BS2YEARS = {
    "Before 1945": (pd.NaT, 1945),
    "1945 - 1969": (1945, 1969),
    "1970 - 1979": (1970, 1979),
    "1980 - 1989": (1980, 1989),
    "1990 - 1999": (1990, 1999),
    "2000 - 2010": (2000, 2010),
    "Post 2010": (2010, pd.NaT),
    "Berfore 1945": (pd.NaT, 1945),
}


@lru_cache(maxsize=1)
def path_cm_dir() -> Path:
    pth = Path(os.environ["CM_REFURBISH_DIR"]).resolve()
    os.makedirs(pth, exist_ok=True)
    return pth


def path_building_stock() -> Path:
    """Return the path to the building stock dataset."""
    return path_cm_dir() / os.environ.get("BUILSTK", "building_stock.csv")


@lru_cache()
def get_building_stock() -> pd.DataFrame:
    """Return building_stock dataframe"""
    logging.info(f"Reading building_stock data from: {path_building_stock()}")
    bs = pd.read_csv(path_building_stock(), sep="|", index_col=0)
    # fix label adding a space
    bs.loc[
        bs["btype"] == "Single family- Terraced houses", "btype"
    ] = "Single family - Terraced houses"

    starts = []
    ends = []
    for _, agekey in bs["bage"].items():
        s, e = (pd.NaT, pd.NaT) if pd.isnull(agekey) else BS2YEARS[agekey]
        starts.append(s)
        ends.append(e)
    bs["start"] = starts
    bs["end"] = ends
    return bs


def path_population() -> Path:
    """Return the path to the population dataset."""
    return path_cm_dir() / os.environ.get("POPGJSN", "LAU_RG_01M_2020_4326.geojson")


@lru_cache()
def get_population() -> gpd.GeoDataFrame:
    """Return building_stock dataframe"""
    logging.info(f"Reading population data from: {path_population()}")
    return gpd.read_file(path_population(), crs="EPSG:4326")


@lru_cache()
def get_population_centroids() -> gpd.GeoDataFrame:
    """Return building_stock dataframe"""
    logging.info("Computing population centroids")
    return get_population().to_crs("EPSG:3035").centroid.to_crs("EPSG:4326")


def path_tabula_Umean() -> Path:
    """Return the path to TABULA/Episcope dataset."""
    return path_cm_dir() / os.environ.get("TABULAX", "tabula-umean.csv")


@lru_cache()
def get_tabula_Umean() -> pd.DataFrame:
    """Return building_stock dataframe"""
    tab = pd.read_csv(path_tabula_Umean(), sep="|", index_col=0)
    # harmonize building types
    tab["bstype"] = ""
    for label, vals in BS2TABULA.items():
        for val in vals:
            idx = tab["btype"] == val
            tab.loc[idx, "bstype"] = label
    return tab


def get_laus(
    user_selection: geometry.Polygon, lau: gpd.GeoDataFrame, centroids: gpd.GeoDataFrame
):
    """Identify the LAU2 from the user selection"""
    # check which LAU2 contains the user selection centroid
    # if user is selecting using the LAU2
    ucentroid = user_selection.to_crs("EPSG:3035").centroid.to_crs("EPSG:4326").iloc[0]
    logging.info(ucentroid)
    idx_contains = lau.contains(ucentroid)
    logging.info(
        "Number of LAU2 that contains the centroid of the "
        f"user selection are: {idx_contains.sum()}"
    )
    laus0 = lau.loc[idx_contains, :]
    # check which LAU2 centroids are contained in the user selection
    # if the user is selecting using NUTS{1|2|3}
    # TODO: running the test raise an error:
    # laus1 = lau.loc[centroids.within(user_selection.iloc[0].geometry), :]
    laus1 = lau.loc[centroids.within(user_selection.iloc[0]), :]
    if len(laus1) == 0:
        # user is selecting using LAU2
        laus = laus0
    else:
        laus = laus1
    return laus


def find_years_range(
    df: pd.DataFrame,
    country_code: str,
    bstype: str,
    start_year: int,
    end_year: int,
    start_col: str = "start",
    end_col: str = "end",
    country_col: str = "country_code",
    bstype_col: str = "btype",
) -> Tuple[int, int]:
    """Return a tuple with the start and end year of dataframe classes"""
    sel = df.loc[
        (
            (df[country_col].str.lower() == country_code.lower())
            & (df[bstype_col] == bstype)
        )
    ]
    syears = (
        sel[start_col]
        .drop_duplicates()
        .dropna()
        .astype(int)
        .sort_values()
        .reset_index(drop=True)
    )
    eyears = (
        sel[end_col]
        .drop_duplicates()
        .dropna()
        .astype(int)
        .sort_values()
        .reset_index(drop=True)
    )
    start_valid = syears[syears.loc[syears > start_year].index[0] - 1]
    end_valid = eyears[eyears.loc[eyears < end_year].index[-1] + 1]
    return start_valid, end_valid


def yearly_savings(
    h_nbuildings: pd.Series,
    c_nbuildings: pd.Series,
    char: pd.DataFrame,
    hdds: float,
    cdds: float,
    perc_basic: float,
    perc_advance: float,
) -> pd.DataFrame:
    """Compute the yearly savings"""
    # Compute yearly energy consumption Wh
    yr_h_enrg = (
        h_nbuildings * char["U mean [W/(m²K)]"] * char["Tot. surface [m²]"]
    ).unstack() * hdds
    yr_c_enrg = (
        c_nbuildings * char["U mean [W/(m²K)]"] * char["Tot. surface [m²]"]
    ).unstack() * cdds
    # h_enrg:
    # rtype                                  ar             cs            ur
    # epoch     bstype
    # 1961-1975 Appartment blocks  66451.218408  261821.360899  83587.183606
    # 1976-1990 Appartment blocks  66631.973998  186896.685536  83654.879461

    # consider only the user defined refurbish rate
    yr_h_savings_ur = (yr_h_enrg["cs"] - yr_h_enrg["ur"]) * (perc_basic / 100.0)
    yr_h_savings_ar = (yr_h_enrg["cs"] - yr_h_enrg["ar"]) * (perc_advance / 100.0)

    yr_c_savings_ur = (yr_c_enrg["cs"] - yr_c_enrg["ur"]) * (perc_basic / 100.0)
    yr_c_savings_ar = (yr_c_enrg["cs"] - yr_c_enrg["ar"]) * (perc_advance / 100.0)

    resdf = pd.DataFrame(
        [
            (demand_type, zone, refurbish_type, epoch, building_type, value)
            for demand_type, data, refurbish_type in zip(
                ["heating", "heating", "cooling", "cooling"],
                [yr_h_savings_ur, yr_h_savings_ar, yr_c_savings_ur, yr_c_savings_ar],
                [
                    "usual refurbish",
                    "advance refurbish",
                    "usual refurbish",
                    "advance refurbish",
                ],
            )
            for (epoch, building_type, zone), value in data.items()
        ],
        columns=[
            "savings_type",
            "zone",
            "refurbish_type",
            "epoch",
            "building_type",
            "savings",
        ],
    )
    return resdf


def hc_sruface(
    bstk: pd.DataFrame,
    cntr_code: str,
    bstype: str,
    bsyear: int,
    beyear: int,
    cntr_pop: float,
    sel_pop: float,
) -> Tuple[float, float]:
    """Compute the heating and cooling surface in m²"""
    hbsel = bstk.loc[
        (
            (bstk["country_code"] == cntr_code.lower())
            & (bstk["btype"] == bstype)
            # & (bstk["bage"] == "1970 - 1979")
            & (bstk["start"] >= bsyear)
            & (bstk["end"] <= beyear)
            & (bstk["unit"] == "Mm²")
            & (bstk["type"] == "Heated area [Mm²]")
        )
    ]
    logging.info(hbsel)

    cbsel = bstk.loc[
        (
            (bstk["country_code"] == cntr_code.lower())
            & (bstk["btype"] == bstype)
            # & (bstk["bage"] == "1970 - 1979")
            & (bstk["start"] >= bsyear)
            & (bstk["end"] <= beyear)
            & (bstk["unit"] == "Mm²")
            & (bstk["type"] == "Cooled area [Mm²]")
        )
    ]
    logging.info(cbsel)

    heating_m2 = hbsel["value"].sum() * 1_000_000.0 / cntr_pop * sel_pop
    cooling_m2 = cbsel["value"].sum() * 1_000_000.0 / cntr_pop * sel_pop
    return heating_m2, cooling_m2


def extract_building_characteristics(
    tabula: pd.DataFrame,
    cntr_code: str,
    bstype: str,
    start_year: int,
    end_year: int,
    cntr_pop: float,
    sel_pop: float,
    start_col: str = "start",
    end_col: str = "end",
    country_col: str = "country",
    bstype_col: str = "bstype",
):
    """Extract building characteristics from TABULA/Episcope dataset"""
    # extract tabula start and end years
    tsyear, teyear = find_years_range(
        df=tabula,
        country_code=cntr_code,
        bstype=bstype,
        start_year=start_year,
        end_year=end_year,
        start_col="start",
        end_col="end",
        country_col="country",
        bstype_col="bstype",
    )

    staby = tabula.loc[
        (
            (tabula["country"] == cntr_code.upper())
            & (tabula["bstype"] == bstype)
            & (tabula["start"].astype(int) >= tsyear)
            & (tabula["end"].astype(int) <= teyear)
        ),
    ]

    grp = staby.groupby(by=["epoch", "bstype", "zone", "rtype"])
    char = grp[
        ["actual_floor_value1", "U mean [W/(m²K)]", "Tot. surface [m²]", "a_c_ref"]
    ].mean()
    return char


def dd_stats(
    lon: float, lat: float, rcp: str, dd_type: str, t_base: float, refyear: int
) -> Tuple[pd.Series, float]:
    """Extract Degree Days value from HDDs and CDDs repository"""
    dd_path = cm_hddcdd.get_datadir(
        datarepository=cm_hddcdd.get_datarepodir(),
        sim_type=rcp,
        dd_type=dd_type,
        Tb=t_base,
    )
    # extract HDDs
    avg_dds = cm_hddcdd.extract_by_dir(gdir=dd_path, lon=lon, lat=lat, refyear=refyear)
    # Multiply by 10 to rescale values back to original
    avg_dds = avg_dds.astype(int) * 10
    # get total annual reference year value
    dds = avg_dds.sum()
    return avg_dds, dds


def __monthly_savings(
    saving_type: str,
    nbuildings: pd.Series,
    char: pd.DataFrame,
    mnth_dds: pd.Series,
    perc_basic: float,
    perc_advance: float,
) -> pd.DataFrame:
    """Compute monthly savings based on refurbish rate and types"""
    mnth = nbuildings * char["U mean [W/(m²K)]"] * char["Tot. surface [m²]"]
    mnth_enrg = pd.DataFrame(
        [
            (saving_type, epoch, bstype, zone, rtype, yrmnth, val * dds)
            for (epoch, bstype, zone, rtype), val in mnth.items()
            for (yrmnth, dds) in mnth_dds.items()
        ],
        columns=[
            "savings_type",
            "epoch",
            "building_type",
            "climatic_zone",
            "refurbish_type",
            "yrmnth",
            "savings",
        ],
    ).set_index(["savings_type", "epoch", "building_type", "climatic_zone", "yrmnth"])

    d_mth_e = {k: v["savings"] for k, v in mnth_enrg.groupby("refurbish_type")}
    # Usual refurbish
    m_savings_ur = (d_mth_e["cs"] - d_mth_e["ur"]) * (perc_basic / 100.0)
    m_savings_ur_df = m_savings_ur.reset_index()
    m_savings_ur_df["refurbish_type"] = "ur"
    # Advance refurbish
    m_savings_ar = (d_mth_e["cs"] - d_mth_e["ar"]) * (perc_advance / 100.0)
    m_savings_ar_df = m_savings_ar.reset_index()
    m_savings_ar_df["refurbish_type"] = "ar"
    return pd.concat([m_savings_ur_df, m_savings_ar_df], ignore_index=True)


def monthly_savings(
    h_nbuildings: pd.Series,
    c_nbuildings: pd.Series,
    char: pd.DataFrame,
    h_mnth_dds: pd.Series,
    c_mnth_dds: pd.Series,
    perc_basic: float,
    perc_advance: float,
) -> pd.DataFrame:
    """Compute the monthly savings"""
    if len(h_mnth_dds) == 12:
        m_h_savings = __monthly_savings(
            saving_type="heating",
            nbuildings=h_nbuildings,
            char=char,
            mnth_dds=h_mnth_dds,
            perc_basic=perc_basic,
            perc_advance=perc_advance,
        )
    else:
        m_h_savings = pd.DataFrame(
            columns=[
                "savings_type",
                "epoch",
                "building_type",
                "climatic_zone",
                "yrmnth",
                "savings",
                "refurbish_type",
            ]
        )

    if len(h_mnth_dds) == 12:
        m_c_savings = __monthly_savings(
            saving_type="cooling",
            nbuildings=c_nbuildings,
            char=char,
            mnth_dds=c_mnth_dds,
            perc_basic=perc_basic,
            perc_advance=perc_advance,
        )
    else:
        m_c_savings = pd.DataFrame(
            columns=[
                "savings_type",
                "epoch",
                "building_type",
                "climatic_zone",
                "yrmnth",
                "savings",
                "refurbish_type",
            ]
        )
    return pd.concat([m_h_savings, m_c_savings], ignore_index=True)


def prepare_output(
    yrly_savings: pd.DataFrame,
    mnth_savings: pd.DataFrame,
    warnings: List[Tuple[str, str]] = None,
) -> Dict[str, Any]:
    """Transform the CM results into the platform's payload"""
    # prepare the CM output
    ret = dict()
    ret["graphs"] = [
        {
            f"Savings on {savings_type} | {refurbish_type}"
            f" | {building_type} | {zone}": dict(
                type="bar",
                values=[
                    (e, v) for _, (e, v) in vals.loc[:, ["epoch", "savings"]].iterrows()
                ],
            )
            for (
                savings_type,
                refurbish_type,
                building_type,
                zone,
            ), vals in yrly_savings.groupby(
                ["savings_type", "refurbish_type", "building_type", "zone"]
            )
        },
    ]
    # ret["graphs"]["Title"] = {}
    # ret["graphs"]["Title"]["type"] = "line"
    # ret["graphs"]["Title"]["values"] = [(xlabel0, yvalue0), (xlabel1, yvalue1), ]

    ret["geofiles"] = {}

    ret["values"] = {
        f"Savings on {savings_type}\n{refurbish_type}"
        f"\n{building_type}\n{epoch}\n{zone}": savings
        for _, (
            savings_type,
            zone,
            refurbish_type,
            epoch,
            building_type,
            savings,
        ) in yrly_savings.iterrows()
    }

    ret["values"].update({k: v for k, v in warnings})

    return validate(ret)


def ref_rate(
    geo,
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
    # check user selected percetage
    basic = perc_basic / 100.0
    advance = perc_advance / 100.0
    if basic > 1.0:
        raise ValueError("Percentage of basic refurbish must be <= 100.")
    if advance > 1.0:
        raise ValueError("Percentage of advance refurbish must be <= 100.")
    if (basic + advance) > 1:
        raise ValueError(
            "The sum of percentage of basic and advance refurbish must be <= 100."
        )
    # start reading the data
    # transform dict to shapely geometry
    user_selection = geo
    # get population data
    pop = get_population()
    # get population centroids
    centroids = get_population_centroids()
    logging.info(centroids)
    # get building stock
    bstk = get_building_stock()
    # get tabula values
    tab = get_tabula_Umean()

    # select the LAUs selected by the user
    laus = get_laus(user_selection, pop, centroids)

    # get and check the country code
    cntr_code = laus["CNTR_CODE"].drop_duplicates()
    logging.info(cntr_code)
    if len(cntr_code) > 1:
        # TODO: handle selection with multiple country involved
        raise ValueError(f"Multiple countries selection ({cntr_code}) not supported")

    # extract the total population numbers
    cntr_code = cntr_code.iloc[0]
    cntr_pop = pop.loc[pop["CNTR_CODE"] == cntr_code, "POP_2020"].sum()
    sel_pop = laus["POP_2020"].sum()

    # extract building stock start and end years
    bsyear, beyear = find_years_range(
        df=bstk,
        country_code=cntr_code,
        bstype=bstype,
        start_year=start_year,
        end_year=end_year,
        start_col="start",
        end_col="end",
    )

    # compute heating cooling surfaces
    heating_m2, cooling_m2 = hc_sruface(
        bstk=bstk,
        cntr_code=cntr_code,
        bstype=bstype,
        bsyear=bsyear,
        beyear=beyear,
        cntr_pop=cntr_pop,
        sel_pop=sel_pop,
    )

    # extract building characteristics from tabula
    char = extract_building_characteristics(
        tabula=tab,
        cntr_code=cntr_code,
        bstype=bstype,
        start_year=start_year,
        end_year=end_year,
        cntr_pop=cntr_pop,
        sel_pop=sel_pop,
    )

    # ASSUMPTION: we do not know the m² per epoch,
    # since the epoch in tabula and the epoch in the bstk do not match!
    # therefore we assume that the m² are equally distributed among the epoch class
    # char.index.levels[0]: ['1961-1975', '1976-1990']
    epochs = char.index.levels[0]
    # h&c m² per tabula epoch of constructions
    h_m2 = heating_m2 / len(epochs)
    c_m2 = cooling_m2 / len(epochs)

    # a_c_ref:energy reference area: conditioned floor area
    h_nbuildings = (h_m2 / char["a_c_ref"]).round(0)
    c_nbuildings = (c_m2 / char["a_c_ref"]).round(0)
    # h_nbuildings:
    #     epoch      bstype             rtype
    #     1961-1975  Appartment blocks  ar       45.0
    #                                   cs       45.0
    #                                   ur       45.0
    #     1976-1990  Appartment blocks  ar       41.0
    #                                   cs       41.0
    #                                   ur       41.0

    # Compute the centroid of the geometry selected by the user
    lon, lat = cm_hddcdd.compute_centroid(geo)

    # retrieve HDDs and CDDs
    avg_hdds, hdds = dd_stats(
        lon=lon, lat=lat, rcp=rcp, dd_type="hdd", t_base=t_base_h, refyear=refyear
    )
    avg_cdds, cdds = dd_stats(
        lon=lon, lat=lat, rcp=rcp, dd_type="cdd", t_base=t_base_c, refyear=refyear
    )

    # compute yearly savings
    yrly_savings = yearly_savings(
        h_nbuildings=h_nbuildings,
        c_nbuildings=c_nbuildings,
        char=char,
        hdds=hdds,
        cdds=cdds,
        perc_basic=perc_basic,
        perc_advance=perc_advance,
    )

    warnings = []
    if len(avg_hdds) < 12:
        warnings.append(
            (
                "WARNING: "
                "Some HDDs months are missing, please select another reference year",
                0,
            )
        )
    if len(avg_cdds) < 12:
        warnings.append(
            (
                "WARNING: "
                "Some HDDs months are missing, please select another reference year",
                0,
            )
        )

    # compute monthly savings
    mnth_savings = monthly_savings(
        h_nbuildings=h_nbuildings,
        c_nbuildings=c_nbuildings,
        char=char,
        h_mnth_dds=avg_hdds,
        c_mnth_dds=avg_cdds,
        perc_basic=perc_basic,
        perc_advance=perc_advance,
    )

    res = prepare_output(yrly_savings, mnth_savings, warnings)
    logging.info(res)
    return res
