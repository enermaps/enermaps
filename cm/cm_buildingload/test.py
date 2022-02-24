import json
import os
import unittest
from copy import deepcopy

import pandas as pd

import buildingload

GEOJSON = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              11.351151466369629,
              46.493872168136285
            ],
            [
              11.361966133117676,
              46.493872168136285
            ],
            [
              11.361966133117676,
              46.50081463609722
            ],
            [
              11.351151466369629,
              46.50081463609722
            ],
            [
              11.351151466369629,
              46.493872168136285
            ]
          ]
        ]
      }
    }
  ]
}


def load_geojson(test_filename):
    test_geojson = buildingload.TESTDATA_DIR / test_filename
    with open(test_geojson) as fd:
        return json.load(fd)


class TestCM(unittest.TestCase):
    def test__compute_centroid(self):
        gj = deepcopy(GEOJSON)
        cx, cy = buildingload.compute_centroid(gj)
        #self.assertAlmostEqual(cx, round(11.35548, ndigits=buildingload.DECIMALS))
        #self.assertAlmostEqual(cy, round(46.49665, ndigits=buildingload.DECIMALS))

        # remove geometry => raise an error
        gj["features"][0].pop("geometry")
        with self.assertRaises(ValueError):
            buildingload.compute_centroid(gj)

    def test__countrycode(self):
        gj = deepcopy(GEOJSON)
        country_code = buildingload.countrycode(
#            geojson=gj,
            lat=46.49665,
            lon=11.35548
        )

    def test__buildingload(self):
        gj = deepcopy(GEOJSON)
        res = buildingload.buildingload(
            geojson=gj,
            building_type="SFH",
            construction_year=2020,
            gfa_external=100.0,
            n_stories=1,
            t_set_min=20.0,
            t_set_max=26.0,
            user_month="January",
            user_week="Week 1",
            user_day="Monday",
            user_model_length="Day",
            roof_type_orientation="0",
            user_roof_pitch=30.0,
            w_f_r=1.3,
            L=1,
            W=1,
            facade_orientation="north",
            a_door=2.0,
            window_front_proportion=10.0,
            window_back_proportion=25.0,
            window_side_1_proportion=25.0,
            window_side_2_proportion=25.0
        )
        from pprint import pprint

        pprint(res)


if __name__ == "__main__":
    unittest.main()