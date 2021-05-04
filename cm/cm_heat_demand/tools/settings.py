from os.path import abspath, dirname, join

TOOLS_DIR = dirname(abspath(__file__))
CM_DIR = dirname(TOOLS_DIR)
TESTDATA_DIR = join(CM_DIR, "testdata")
