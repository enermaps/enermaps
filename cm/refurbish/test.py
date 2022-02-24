import os
import unittest
from copy import deepcopy

import geopandas as gpd
import pandas as pd
from BaseCM import cm_hddcdd as hc

import refurbish as rf
from schema import get_refurbish_schema

# shared data among the tests
GEOJSON = {
    "features": [
        {
            "geometry": {
                "coordinates": [
                    [
                        [11.061588, 45.567844],
                        [11.055015, 45.563899],
                        [11.050421, 45.565349],
                        [11.040453, 45.560869],
                        [11.032734, 45.561389],
                    ]
                ],
                "type": "Polygon",
            },
            "id": 80284,
            "properties": {
                "ds_id": 0,
                "dt": "",
                "fields": "",
                "id": "IT_023038",
                "layer": '{ "type": "numerical" }',
                "start_at": "",
                "units": '{ "": null }',
                "variables": '{ "": 0 }',
                "z": "",
            },
            "type": "Feature",
        }
    ],
    "type": "FeatureCollection",
}


char = pd.DataFrame.from_dict(
    {
        "epoch": {
            0: "1946-1960",
            1: "1946-1960",
            2: "1946-1960",
            3: "1961-1975",
            4: "1961-1975",
            5: "1961-1975",
        },
        "bstype": {
            0: "Multifamily houses",
            1: "Multifamily houses",
            2: "Multifamily houses",
            3: "Multifamily houses",
            4: "Multifamily houses",
            5: "Multifamily houses",
        },
        "zone": {
            0: "MidClim",
            1: "MidClim",
            2: "MidClim",
            3: "MidClim",
            4: "MidClim",
            5: "MidClim",
        },
        "rtype": {0: "ar", 1: "cs", 2: "ur", 3: "ar", 4: "cs", 5: "ur"},
        "actual_floor_value1": {
            0: 320.4,
            1: 320.4,
            2: 320.4,
            3: 186.7,
            4: 186.7,
            5: 186.7,
        },
        "U mean [W/(m²K)]": {
            0: 0.372017679025645,
            1: 1.59023793327478,
            2: 0.454842496211203,
            3: 0.318526227666346,
            4: 1.33964886264575,
            5: 0.403038192190635,
        },
        "Tot. surface [m²]": {
            0: 1569.1,
            1: 1569.1,
            2: 1569.1,
            3: 1667.4,
            4: 1667.4,
            5: 1667.4,
        },
        "a_c_ref": {
            0: 817.105,
            1: 817.105,
            2: 817.105,
            3: 793.9,
            4: 793.9,
            5: 793.9,
        },
    }
).set_index(["epoch", "bstype", "zone", "rtype"])

avg_hdds = pd.Series(
    name="cx=4402854.721,cy=2495189.541",
    index=[
        "2021-01",
        "2021-02",
        "2021-03",
        "2021-04",
        "2021-05",
        "2021-06",
        "2021-07",
        "2021-08",
        "2021-09",
        "2021-10",
        "2021-11",
        "2021-12",
    ],
    data=[410, 300, 250, 150, 70, 30, 20, 30, 70, 170, 320, 420],
    dtype="int",
)

avg_cdds = pd.Series(
    name="cx=4402854.721,cy=2495189.541",
    index=[
        "2021-01",
        "2021-02",
        "2021-03",
        "2021-04",
        "2021-05",
        "2021-06",
        "2021-07",
        "2021-08",
        "2021-09",
        "2021-10",
        "2021-11",
        "2021-12",
    ],
    data=[0, 0, 0, 0, 0, 10, 20, 10, 0, 0, 0, 0],
    dtype="int",
)

h_nbuildings = pd.Series(
    [15.0, 15.0, 15.0, 15.0, 15.0, 15.0],
    index=pd.MultiIndex.from_tuples(
        [
            ("1946-1960", "Multifamily houses", "MidClim", "ar"),
            ("1946-1960", "Multifamily houses", "MidClim", "cs"),
            ("1946-1960", "Multifamily houses", "MidClim", "ur"),
            ("1961-1975", "Multifamily houses", "MidClim", "ar"),
            ("1961-1975", "Multifamily houses", "MidClim", "cs"),
            ("1961-1975", "Multifamily houses", "MidClim", "ur"),
        ],
        names=["epoch", "bstype", "zone", "rtype"],
    ),
)


c_nbuildings = pd.Series(
    [2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
    index=pd.MultiIndex.from_tuples(
        [
            ("1946-1960", "Multifamily houses", "MidClim", "ar"),
            ("1946-1960", "Multifamily houses", "MidClim", "cs"),
            ("1946-1960", "Multifamily houses", "MidClim", "ur"),
            ("1961-1975", "Multifamily houses", "MidClim", "ar"),
            ("1961-1975", "Multifamily houses", "MidClim", "cs"),
            ("1961-1975", "Multifamily houses", "MidClim", "ur"),
        ],
        names=["epoch", "bstype", "zone", "rtype"],
    ),
)

yrly_savings = pd.DataFrame.from_dict(
    {
        "savings_type": {
            0: "heating",
            1: "heating",
            2: "heating",
            3: "heating",
            4: "cooling",
            5: "cooling",
            6: "cooling",
            7: "cooling",
        },
        "zone": {
            0: "MidClim",
            1: "MidClim",
            2: "MidClim",
            3: "MidClim",
            4: "MidClim",
            5: "MidClim",
            6: "MidClim",
            7: "MidClim",
        },
        "refurbish_type": {
            0: "usual refurbish",
            1: "usual refurbish",
            2: "advance refurbish",
            3: "advance refurbish",
            4: "usual refurbish",
            5: "usual refurbish",
            6: "advance refurbish",
            7: "advance refurbish",
        },
        "epoch": {
            0: "1946-1960",
            1: "1961-1975",
            2: "1946-1960",
            3: "1961-1975",
            4: "1946-1960",
            5: "1961-1975",
            6: "1946-1960",
            7: "1961-1975",
        },
        "building_type": {
            0: "Multifamily houses",
            1: "Multifamily houses",
            2: "Multifamily houses",
            3: "Multifamily houses",
            4: "Multifamily houses",
            5: "Multifamily houses",
            6: "Multifamily houses",
            7: "Multifamily houses",
        },
        "savings": {
            0: 3367127.572760307,
            1: 2951621.7543228636,
            2: 722550.5535561962,
            3: 643590.3152314408,
            4: 7126.195921185834,
            5: 6246.818527667436,
            6: 1529.207520753854,
            7: 1362.0959052517264,
        },
    }
)

payload = {
    "geofiles": {},
    "graphs": [
        {
            "Savings on cooling | advance refurbish | Multifamily houses | MidClim": {
                "type": "bar",
                "values": [
                    ("1946-1960", 1146.9056405653903),
                    ("1961-1975", 1021.571928938795),
                ],
            },
            "Savings on cooling | usual refurbish | Multifamily houses | MidClim": {
                "type": "bar",
                "values": [
                    ("1946-1960", 5344.646940889375),
                    ("1961-1975", 4685.113895750577),
                ],
            },
            "Savings on heating | advance refurbish | Multifamily houses | MidClim": {
                "type": "bar",
                "values": [
                    ("1946-1960", 642267.1587166189),
                    ("1961-1975", 572080.2802057252),
                ],
            },
            "Savings on heating | usual refurbish | Multifamily houses | MidClim": {
                "type": "bar",
                "values": [
                    ("1946-1960", 2993002.2868980514),
                    ("1961-1975", 2623663.781620323),
                ],
            },
        }
    ],
    "values": {
        "Savings on cooling\nadvance refurbish\nMultifamily houses\n1946-1960\nMidClim": 1146.9056405653903,
        "Savings on cooling\nadvance refurbish\nMultifamily houses\n1961-1975\nMidClim": 1021.571928938795,
        "Savings on cooling\nusual refurbish\nMultifamily houses\n1946-1960\nMidClim": 5344.646940889375,
        "Savings on cooling\nusual refurbish\nMultifamily houses\n1961-1975\nMidClim": 4685.113895750577,
        "Savings on heating\nadvance refurbish\nMultifamily houses\n1946-1960\nMidClim": 642267.1587166189,
        "Savings on heating\nadvance refurbish\nMultifamily houses\n1961-1975\nMidClim": 572080.2802057252,
        "Savings on heating\nusual refurbish\nMultifamily houses\n1946-1960\nMidClim": 2993002.2868980514,
        "Savings on heating\nusual refurbish\nMultifamily houses\n1961-1975\nMidClim": 2623663.781620323,
    },
}


class TestCM(unittest.TestCase):
    def test__get_refurbish_schema(self):
        schema = get_refurbish_schema(save=False)
        self.assertIn("properties", schema)
        props = schema["properties"]
        # check basic attributes
        for _, val in props.items():
            for key in ("type", "title", "description", "default"):
                self.assertIn(key, val)
        # check for specifiv parameters
        params = [
            # param_name     | check_enum  | check_minmax
            ("reference year", True, True),
            ("start epoch of construction", False, False),
            ("end epoch of construction", False, False),
            ("percentage basic refurbish rate", False, True),
            ("percentage advance refurbish rate", False, True),
        ]
        for param_name, check_enum, check_minmax in params:
            self.assertIn(param_name, props)
            param = props[param_name]
            if check_enum:
                self.assertIn("enum", param)
            if check_minmax:
                for key in ("minimum", "maximum"):
                    self.assertIn(key, param)

    def test__get_building_stock(self):
        bstk = rf.get_building_stock()
        cols = [
            "country_code",
            "sector",
            "subsector",
            "btype",
            "bage",
            "topic",
            "feature",
            "type",
            "detail",
            "estimated",
            "value",
            "unit",
            "source",
            "start",
            "end",
        ]
        for col in cols:
            self.assertIn(col, bstk.columns)
        self.assertGreaterEqual(len(bstk["country_code"].drop_duplicates()), 27)

    def test__get_population(self):
        pop = rf.get_population()
        cols = [
            "id",
            "GISCO_ID",
            "CNTR_CODE",
            "LAU_ID",
            "LAU_NAME",
            "POP_2020",
            "POP_DENS_2020",
            "AREA_KM2",
            "YEAR",
            "FID",
            "geometry",
        ]
        for col in cols:
            self.assertIn(col, pop.columns)
        self.assertGreaterEqual(len(pop["CNTR_CODE"].drop_duplicates()), 27)

    def test__get_population_centroids(self):
        centroids = rf.get_population_centroids()
        self.assertEqual(centroids.geom_type[0], "Point")
        self.assertEqual(centroids.crs.to_epsg(), 4326)

    def test__get_tabula(self):
        tab = rf.get_tabula_Umean()
        cols = [
            "country",
            "bstype",
            "start",
            "end",
            "zone",
            "btype",
            "epoch",
            "actual_floor_value1",
            "U mean [W/(m²K)]",
            "Tot. surface [m²]",
            "a_c_ref",
        ]
        for col in cols:
            self.assertIn(col, tab.columns)
        self.assertGreaterEqual(len(tab["country"].drop_duplicates()), 21)

    def test__get_laus(self):
        gj = deepcopy(GEOJSON)
        user_selection = gpd.GeoDataFrame.from_features(
            gj["features"], crs="EPSG:4326"
        ).geometry
        pop = rf.get_population()
        centroids = rf.get_population_centroids()
        laus = rf.get_laus(user_selection, pop, centroids)
        self.assertEqual(laus.index[0], 77189)
        self.assertEqual(laus.loc[:, "LAU_ID"].iloc[0], "023038")

    def test__find_years_range(self):
        bsyear, beyear = rf.find_years_range(
            df=rf.get_building_stock(),
            country_code="IT",
            bstype="Multifamily houses",
            start_year=1960,
            end_year=1969,
            start_col="start",
            end_col="end",
        )
        self.assertEqual(bsyear, 1945)
        self.assertEqual(beyear, 1969)

    def test__hc_surface(self):
        heating_m2, cooling_m2 = rf.hc_sruface(
            bstk=rf.get_building_stock(),
            cntr_code="IT",
            bstype="Multifamily houses",
            bsyear=1945,
            beyear=1969,
            cntr_pop=60244639.0,
            sel_pop=10838.0,
        )
        self.assertEqual(heating_m2, 24536.38790994685)
        self.assertEqual(cooling_m2, 2752.904475699489)

    def test__extract_building_characteristics(self):
        tchar = rf.extract_building_characteristics(
            tabula=rf.get_tabula_Umean(),
            cntr_code="IT",
            bstype="Multifamily houses",
            start_year=1960,
            end_year=1969,
            cntr_pop=60244639.0,
            sel_pop=10838.0,
        )
        pd.testing.assert_frame_equal(tchar, char)

    def test__dd_stats(self):
        tavg_hdds, thdds = rf.dd_stats(
            lon=11.047,
            lat=45.564,
            rcp="historical",
            dd_type="hdd",
            t_base=15.0,
            refyear=2021,
        )
        self.assertEqual(thdds, 2240)
        pd.testing.assert_series_equal(tavg_hdds, avg_hdds)

    def test__yearly_savings(self):
        tyrly_savings = rf.yearly_savings(
            h_nbuildings=h_nbuildings.copy(),
            c_nbuildings=c_nbuildings.copy(),
            char=char.copy(),
            hdds=2520,
            cdds=40,
            perc_basic=5.0,
            perc_advance=1.0,
        )
        pd.testing.assert_frame_equal(tyrly_savings, yrly_savings)

    def test__ref_rate(self):
        """
        # ref_rate
        res = ref_rate(
            geo=geo4326,
            bstype=params.get("building typology", "Appartment blocks"),
            start_year=params.get("start epoch of construction", 1960),
            end_year=params.get("end epoch of construction", 1969),
            perc_basic=params.get("percentage basic refurbish rate", 10.0),
            perc_advance=params.get("percentage advance refurbish rate", 5.0),
            refyear=params.get("reference year", 2050),
            rcp=params.get("scenario RCP", "historical"),
            t_base_h=params.get("base temperature for HDD", 18.0),
            t_base_c=params.get("base temperature for CDD", 22.0),
        )
        """
        gj = deepcopy(GEOJSON)
        geo = gpd.GeoDataFrame.from_features(gj["features"], crs="EPSG:4326").geometry
        res = rf.ref_rate(
            geo=geo,
            bstype="Multifamily houses",
            start_year=1960,
            end_year=1969,
            perc_basic=5.0,
            perc_advance=1.0,
            refyear=2021,
            rcp="historical",
            t_base_h=15.0,
            t_base_c=26.0,
        )
        self.assertEqual(res, payload)


if __name__ == "__main__":
    orig_repo = os.environ.get("CM_HDD_CDD_REPOSITORY", None)
    os.environ["CM_HDD_CDD_REPOSITORY"] = hc.TESTDATA_DIR.as_posix()

    unittest.main()

    if orig_repo is None:
        os.environ.pop("CM_HDD_CDD_REPOSITORY")
    else:
        os.environ["CM_HDD_CDD_REPOSITORY"] = orig_repo
