'''
Created on Jul 26, 2017

@author: simulant
'''
import os
import time
import sys
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW20.indexing import calc_index


def main(minx, maxy, dimX, dimY, fminx_, fmaxx_, fminy_, fmaxy_,
         pixWidth=100.0, pixHeight=100.0):
    output = calc_index(minx, maxy, dimX, dimY, fminx_, fmaxx_,
                        fminy_, fmaxy_, pixWidth, pixHeight)
    return output

if __name__ == "__main__":
    start = time.time()
    minx = 4285400
    maxy = 2890500
    dimX = 2953
    dimY = 5692
    fminx_ = 4285406.36383
    fmaxx_ = 4854633.29352
    fminy_ = 2595156.89558
    fmaxy_ = 2890412.7091390
    resolution = 100
    output = main(minx, maxy, dimX, dimY, fminx_, fmaxx_, fminy_, fmaxy_)
    print('lowIndexX = %d \nupIndexX = %d \nlowIndexY = %d \nupIndexY = %d'
          % (output[0], output[1], output[2], output[3]))
    elapsed = time.time() - start
    print("%0.3f seconds" % elapsed)
