import os
import time
import sys
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW21.csv2shp import csv2shapefile as c2s


def main(inShpPath, inCSV, outShpPath, id_field='id', shp_id_field=0,
         OutputSRS=3035):
    c2s(inShpPath, inCSV, outShpPath, id_field, shp_id_field, OutputSRS)


if __name__ == "__main__":
    start = time.time()
    # path to the src
    data_warehouse = path + os.sep + 'AD/data_warehouse'
    inShpPath = data_warehouse + os.sep + "AT_NUTS3.shp"
    inCSV = data_warehouse + os.sep + "CM.TUW.22.csv2shp.csv"
    output_dir = path + os.sep + 'Outputs'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    outShpPath = output_dir + os.sep + "CM_TUW22_csv2shp.shp"
    main(inShpPath, inCSV, outShpPath)
    elapsed = time.time() - start
    print("%0.3f seconds" % elapsed)
