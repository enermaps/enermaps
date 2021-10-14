import json
import os
import unittest
from copy import deepcopy

import pandas as pd

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


def load_geojson(test_filename):
    test_geojson = hc.TESTDATA_DIR / test_filename
    with open(test_geojson) as fd:
        return json.load(fd)


class TestCM(unittest.TestCase):
    def test__compute_centroid(self):
        gj = deepcopy(GEOJSON)
        cx, cy = hc.compute_centroid(gj)
        self.assertAlmostEqual(cx, round(11.0480422, ndigits=hc.DECIMALS))
        self.assertAlmostEqual(cy, round(45.563869999999994, ndigits=hc.DECIMALS))

        # remove geometry => raise an error
        gj["features"][0].pop("geometry")
        with self.assertRaises(ValueError):
            hc.compute_centroid(gj)

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
            / "18.0"
            / "monthly"
            / "average",
            lat=45.563869999999994,
            lon=11.0480422,
        )
        pd.testing.assert_series_equal(
            sr,
            pd.Series(
                name="yp=273,xp=457",
                index=[
                    "2021_01",
                    "2021_02",
                    "2021_03",
                    "2021_04",
                    "2021_05",
                    "2021_06",
                    "2021_07",
                    "2021_08",
                    "2021_09",
                    "2021_10",
                    "2021_11",
                    "2021_12",
                ],
                data=[69, 75, 80, 84, 94, 103, 104, 109, 99, 91, 86, 83],
                dtype="uint8",
            ),
        )

    def test__hdd_cdd_stats(self):
        gj = deepcopy(GEOJSON)
        res = hc.hdd_cdd_stats(
            geojson=gj,
            refyear=2035,
            rcp="historical",
            t_base_h=18.0,
            t_base_c=22.0,
        )
        from pprint import pprint

        pprint(res)


if __name__ == "__main__":
    orig_repo = os.environ.get("CM_HDD_CDD_REPOSITORY", None)
    os.environ["CM_HDD_CDD_REPOSITORY"] = hc.TESTDATA_DIR.as_posix()
    unittest.main()
    os.environ["CM_HDD_CDD_REPOSITORY"] = orig_repo
