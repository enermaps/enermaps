import unittest

import numpy as np

from .areas import MapSizeError, get_browsing_indexes


class TestAreasTools(unittest.TestCase):
    def test_wrong_map_size(self):
        labels_map_size = (2, 3)
        map_size = (2, 2)
        self.assertNotEqual(labels_map_size, map_size)
        with self.assertRaises(MapSizeError):
            get_browsing_indexes(
                labels_array=np.zeros(labels_map_size),
                pixel_filtered_map=np.zeros(map_size),
                labels_number=0,
            )


if __name__ == "__main__":
    unittest.main()
