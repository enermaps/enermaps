import unittest

import numpy as np

from .areas import MapSizeError, get_browsing_indexes


class TestAreasTools(unittest.TestCase):
    def test_wrong_map_size(self):
        """
        Test if a MapSizeError is raised when where the map size
        and the labels map size is not the same.
        """

        labels_map_size = (2, 3)
        map_size = (2, 2)
        self.assertNotEqual(labels_map_size, map_size)
        with self.assertRaises(MapSizeError):
            get_browsing_indexes(
                labels_array=np.zeros(labels_map_size),
                pixel_filtered_map=np.zeros(map_size),
                n_label=0,
            )


if __name__ == "__main__":
    unittest.main()
