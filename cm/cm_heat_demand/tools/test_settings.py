import unittest
from os.path import isdir

from .settings import CM_DIR, TESTDATA_DIR, TOOLS_DIR


class TestSettings(unittest.TestCase):
    def test_directory_path(self):
        """Check if all directory path in the settings file exist."""

        def is_dir(*paths_dir: str):
            for path_dir in paths_dir:
                self.assertTrue(isdir(path_dir))

        is_dir(TESTDATA_DIR, TOOLS_DIR, CM_DIR)


if __name__ == "__main__":
    unittest.main()
