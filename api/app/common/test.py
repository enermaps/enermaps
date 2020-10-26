import os


def get_testdata(filename):
    """Return the absolute location of the filename in the testdatadir
    """
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    testdata_dir = os.path.join(os.path.dirname(current_file_dir), "testdata")
    return os.path.join(testdata_dir, filename)
