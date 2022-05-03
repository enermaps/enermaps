"""See https://docs.python.org/3/library/unittest.html#assert-methods
for more information about 'unittest' framework.
"""
import unittest


class TestEmptyCM(unittest.TestCase):
    """Class with all the unit test made on the CM."""

    def test_data(self):
        """Function performing a unit test."""
        pass


if __name__ == "__main__":
    unittest.main()
