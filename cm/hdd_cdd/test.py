#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest
from copy import deepcopy

import geopandas as gpd
from BaseCM.cm_hddcdd import TESTDATA_DIR

import hddcdd as hc

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


class TestCM(unittest.TestCase):
    def test__hdd_cdd_stats(self):
        self.maxDiff = None
        gj = deepcopy(GEOJSON)
        geo = gpd.GeoDataFrame.from_features(gj["features"], crs="EPSG:4326").geometry
        res = hc.hdd_cdd_stats(
            geo=geo,
            refyear=2035,
            rcp="historical",
            t_base_h=15.0,
            t_base_c=26.0,
        )
        ret = {
            "geofiles": {},
            "graphs": [
                {"Yearly HDDs": {"type": "bar", "values": [("2021", 2240)]}},
                {"Yearly CDDs": {"type": "bar", "values": [("2021", 30)]}},
                {
                    "Monthly HDDs": {
                        "type": "line",
                        "values": [
                            ("2021-01", 410),
                            ("2021-02", 300),
                            ("2021-03", 250),
                            ("2021-04", 150),
                            ("2021-05", 70),
                            ("2021-06", 30),
                            ("2021-07", 20),
                            ("2021-08", 30),
                            ("2021-09", 70),
                            ("2021-10", 170),
                            ("2021-11", 320),
                            ("2021-12", 420),
                        ],
                    }
                },
                {
                    "Monthly CDDs": {
                        "type": "line",
                        "values": [
                            ("2021-01", 0),
                            ("2021-02", 0),
                            ("2021-03", 0),
                            ("2021-04", 0),
                            ("2021-05", 0),
                            ("2021-06", 10),
                            ("2021-07", 10),
                            ("2021-08", 10),
                            ("2021-09", 0),
                            ("2021-10", 0),
                            ("2021-11", 0),
                            ("2021-12", 0),
                        ],
                    }
                },
            ],
            "values": {
                "Yearly CDDs 25%": "30.0",
                "Yearly CDDs 50%": "30.0",
                "Yearly CDDs 75%": "30.0",
                "Yearly CDDs count": "1.0",
                "Yearly CDDs max": "30.0",
                "Yearly CDDs mean": "30.0",
                "Yearly CDDs min": "30.0",
                "Yearly CDDs std": "nan",
                "Yearly HDDs 25%": "2240.0",
                "Yearly HDDs 50%": "2240.0",
                "Yearly HDDs 75%": "2240.0",
                "Yearly HDDs count": "1.0",
                "Yearly HDDs max": "2240.0",
                "Yearly HDDs mean": "2240.0",
                "Yearly HDDs min": "2240.0",
                "Yearly HDDs std": "nan",
            },
        }
        self.assertEqual(res, ret)

        res_empty = hc.hdd_cdd_stats(
            geo=geo,
            refyear=2035,
            rcp="historical",
            t_base_h=4.0,
            t_base_c=40.0,
        )
        ret_empty = {
            "geofiles": {},
            "graphs": [],
            "values": {
                (
                    "WARNING: The selected set of simulation type (historical), "
                    "degree days (cdd) and base temperature (40.0). "
                    "Valid base temperature for this simulation type are:['26.0']"
                ): 0,
                (
                    "WARNING: The selected set of simulation type (historical), "
                    "degree days (hdd) and base temperature (4.0). "
                    "Valid base temperature for this simulation type are:['15.0']"
                ): 0,
                "Yearly CDDs: Dataset not available": 0,
                "Yearly HDDs: Dataset not available": 0,
            },
        }
        self.assertEqual(res_empty, ret_empty)

        res_halfempty = hc.hdd_cdd_stats(
            geo=geo,
            refyear=2035,
            rcp="historical",
            t_base_h=4.0,
            t_base_c=26.0,
        )
        ret_halfempty = {
            "graphs": [
                {"Yearly CDDs": {"type": "bar", "values": [("2021", 30)]}},
                {
                    "Monthly CDDs": {
                        "type": "line",
                        "values": [
                            ("2021-01", 0),
                            ("2021-02", 0),
                            ("2021-03", 0),
                            ("2021-04", 0),
                            ("2021-05", 0),
                            ("2021-06", 10),
                            ("2021-07", 10),
                            ("2021-08", 10),
                            ("2021-09", 0),
                            ("2021-10", 0),
                            ("2021-11", 0),
                            ("2021-12", 0),
                        ],
                    }
                },
            ],
            "geofiles": {},
            "values": {
                (
                    "WARNING: The selected set of simulation type (historical), "
                    "degree days (hdd) and base temperature (4.0). "
                    "Valid base temperature for this simulation type are:['15.0']"
                ): 0,
                "Yearly HDDs: Dataset not available": 0,
                "Yearly CDDs count": "1.0",
                "Yearly CDDs mean": "30.0",
                "Yearly CDDs std": "nan",
                "Yearly CDDs min": "30.0",
                "Yearly CDDs 25%": "30.0",
                "Yearly CDDs 50%": "30.0",
                "Yearly CDDs 75%": "30.0",
                "Yearly CDDs max": "30.0",
            },
        }
        self.assertEqual(res_halfempty, ret_halfempty)


if __name__ == "__main__":
    orig_repo = os.environ.get("CM_HDD_CDD_REPOSITORY", None)
    os.environ["CM_HDD_CDD_REPOSITORY"] = TESTDATA_DIR.as_posix()
    unittest.main()
    os.environ["CM_HDD_CDD_REPOSITORY"] = orig_repo
