#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest
from copy import deepcopy

import geopandas as gpd
import pandas as pd

from BaseCM import cm_hddcdd as hc

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


class TestHddCddSharedFunctions(unittest.TestCase):
    def test__get_years(self):
        years = hc.get_years()
        self.assertEqual(years, [2021])

    def test__get_scenarios(self):
        scenarios = hc.get_scenarios()
        self.assertEqual(scenarios, ["historical"])

    def test__get_base_temperature(self):
        tbase = hc.get_base_temperature("hdd")
        self.assertEqual(tbase, [15.0])

    def test__get_hddcdd_schema(self):
        schema = hc.get_hddcdd_schema(save=False)
        self.assertIn("properties", schema)
        props = schema["properties"]
        for _, val in props.items():
            for key in ("type", "title", "description", "default", "enum"):
                self.assertIn(key, val)

    def test__compute_centroid(self):
        gj = deepcopy(GEOJSON)
        geo = gpd.GeoDataFrame.from_features(gj["features"], crs="EPSG:4326").geometry
        cx, cy = hc.compute_centroid(geo)
        self.assertAlmostEqual(cx, round(11.04713688, ndigits=hc.DECIMALS))
        self.assertAlmostEqual(cy, round(45.56383191, ndigits=hc.DECIMALS))

    def test__reproj(self):
        # https://epsg.io/transform#s_srs=4326&t_srs=3035&x=11.0132789&y=45.5228261
        # (lat, lon)
        # (45.5228261, 11.0132789) => (4400277.98, 2490583.97)
        cx, cy = hc.reproj(
            src_y=11.013279, src_x=45.522826, src_crs="EPSG:4326", dst_crs="EPSG:3035"
        )
        self.assertEqual(f"{cx:.2f}", "4400277.99")
        self.assertEqual(f"{cy:.2f}", "2490583.96")

    def test__get_datarepodir(self):
        self.assertEqual(hc.get_datarepodir(), hc.TESTDATA_DIR)

    def test__get_datadir(self):
        self.assertEqual(
            hc.get_datadir(
                "myrepo",
                sim_type="historical",
                dd_type="hdd",
                Tb=18.0,
                aggr_window="monthly",
                method="average",
            ).as_posix(),
            "myrepo/historical/hdd/18.0/monthly/average",
        )

    def test__extract_by_dir(self):
        sr = hc.extract_by_dir(
            gdir=hc.TESTDATA_DIR
            / "historical"
            / "hdd"
            / "15.0"
            / "monthly"
            / "average",
            lat=45.563869999999994,
            lon=11.0480422,
        )
        pd.testing.assert_series_equal(
            sr,
            pd.Series(
                name="yp=309,xp=283",
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
                data=[41, 30, 25, 15, 7, 3, 2, 3, 7, 17, 32, 42],
                dtype="uint8",
            ),
        )

        # test using the reference year
        sr_yr = hc.extract_by_dir(
            gdir=hc.TESTDATA_DIR
            / "historical"
            / "hdd"
            / "15.0"
            / "monthly"
            / "average",
            lat=45.563869999999994,
            lon=11.0480422,
            refyear=2021,
        )
        pd.testing.assert_series_equal(
            sr_yr,
            pd.Series(
                name="yp=309,xp=283",
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
                data=[41, 30, 25, 15, 7, 3, 2, 3, 7, 17, 32, 42],
                dtype="uint8",
            ),
        )

        # test using the reference month
        sr_yr = hc.extract_by_dir(
            gdir=hc.TESTDATA_DIR
            / "historical"
            / "hdd"
            / "15.0"
            / "monthly"
            / "average",
            lat=45.563869999999994,
            lon=11.0480422,
            refmonth=1,
        )
        pd.testing.assert_series_equal(
            sr_yr,
            pd.Series(
                name="yp=309,xp=283",
                index=["2021-01"],
                data=[41],
                dtype="uint8",
            ),
        )


if __name__ == "__main__":
    orig_repo = os.environ.get("CM_HDD_CDD_REPOSITORY", None)
    os.environ["CM_HDD_CDD_REPOSITORY"] = hc.TESTDATA_DIR.as_posix()

    unittest.main()

    if orig_repo is None:
        os.environ.pop("CM_HDD_CDD_REPOSITORY")
    else:
        os.environ["CM_HDD_CDD_REPOSITORY"] = orig_repo
