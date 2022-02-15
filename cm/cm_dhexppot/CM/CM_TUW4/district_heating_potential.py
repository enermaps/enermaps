# -*- coding: utf-8 -*-
"""
Created on July 11 2017

@author: fallahnejad@eeg.tuwien.ac.at
"""
import os
import sys
import time
import numpy as np
from scipy.ndimage import binary_dilation
from scipy.ndimage import binary_erosion
from scipy.ndimage import binary_fill_holes
from scipy.ndimage import measurements
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW1.read_raster import raster_array as RA
'''
The input for this calculation module is "heat density map" with [MWh/ha]
unit. The output of this calculation module is set of connected pixels to
which the potential of that connected pixels in [GWh] is assigned.
pixel_threshold in [MWh/ha]
DH_threshold in [GWh/year]
'''


def DHRegions(DH, DH_threshold):
    '''
    This code uses the concept of connected components from image processing
    library of Scipy in order to detect the potential district heating areas.
    '''
    # "struct" defines how the connected components can be considered.
    struct = np.ones((3, 3)).astype(int)
    # expansion and erosion of the connected components in order to connect
    # different components which are in close vicinity of each other
    # struct(3,3): 200 meter distance between the two connected components
    DH_expanded = binary_dilation(DH, structure=struct)
    DH_connected = binary_erosion(DH_expanded, structure=struct)
    # fills the holes within the connected components
    #DH_noHole = binary_fill_holes(DH_connected)
    DH_noHole = DH_connected
    # label the connected components
    struct = np.ones((3, 3)).astype(int)
    labels, numLabels = measurements.label(DH_noHole, structure=struct)
    # the conditional statement prevents from error in the following code.
    # This can also be incorporated in order to filter areas smaller than a
    # specific size e.g. 1km2 ~ 100.
    if labels.size > 0:
        # labels start from 1. Therefore, PotDH should have numLabels+1
        # elements
        PotDH = np.zeros((numLabels+1)).astype(bool)
        # using sparse matrix indices to swift the calculation. This helps to
        # implement "np.unique" much faster
        sparseRow, sparseCol = np.nonzero(labels)
        sparseLabels = labels[sparseRow, sparseCol]
        sparseDH = DH[sparseRow, sparseCol]
        # sort sparse values based on sparseLabels. This helps to implement
        # summation process much faster.
        sortedSparseData = np.asarray(sorted(zip(sparseRow, sparseCol,
                                                 sparseLabels, sparseDH),
                                             key=lambda x: x[2]))
        # find unique values and their counts within the sparseLabels
        unique, counts = np.unique(sparseLabels, return_counts=True)
        '''
        calculate starting and ending indices of each unique value in order
        to swift the summation operation. calculate starting and ending
        indices of each unique value in order to swift the summation
        operation. Note that a[st:end] refers to elements of a including "st"
        and excluding end.
        Note: To get the last element of the same type, however, cumsum shoud
        be subtracted by 1:
        (e.g. [1,1,1,1,2,2,2]: hear st for 1 is 0; end for 1 is 4; the last
        element which is one is 3)
        '''
        end = np.cumsum(counts)
        st = np.concatenate((np.zeros((1)), end[0:numLabels-1]))
        
        for i in range(numLabels):
            # sum over sparseDH
            # input: [MWh/ha] for each ha --> summation returns MWh for the
            # coherent area
            pot = np.sum(sortedSparseData[int(st[i]):int(end[i]), 3])
            if pot >= DH_threshold:
                # here should be i+1 because labeling starts from one and not
                # from zero
                PotDH[i+1] = True
        DH_regions = PotDH[labels]
        return DH_regions


def DHPotential(DH_Regions, heat_density_map):
    if isinstance(heat_density_map, np.ndarray):
        hdm_arr = heat_density_map
    elif isinstance(heat_density_map, str):
        hdm_arr, gt = RA(heat_density_map, return_gt=True)
    struct = np.ones((3, 3)).astype(int)
    labels, numLabels = measurements.label(DH_Regions, structure=struct)
    DHPot = np.zeros((numLabels+1)).astype(float)
    sparseRow, sparseCol = np.nonzero(labels)
    # This helps to implement "np.unique" much faster
    sparse_labels = labels[sparseRow, sparseCol]
    sparse_hdm = hdm_arr[sparseRow, sparseCol]
    # sort sparse values based on sparse_labels. This helps to implement
    # summation process much faster.
    sortedSparseData = np.asarray(sorted(zip(sparseRow, sparseCol,
                                             sparse_labels, sparse_hdm),
                                        key=lambda x: x[2]))
    unique, counts = np.unique(sparse_labels, return_counts=True)
    end = np.cumsum(counts)
    st = np.concatenate((np.zeros((1)), end[0:numLabels-1]))
    for i in range(numLabels):
        # input: [MWh/ha] for each ha --> to get potential in GWh it
        # should be multiplied by 0.001
        DHPot[i+1] = 0.001 * np.sum(sortedSparseData[int(st[i]):int(end[i]), 3])
    #DH_Potential = DHPot[labels]
    DHPot = DHPot[1::]
    # potential of each coherent area in GWh is assigned to its pixels
    return DHPot, labels


def DHReg(heat_density_map, pix_threshold, DH_threshold, in_orig=None):
    # Factor 1000 for conversion from GWh/a to MWh/a
    DH_threshold = DH_threshold * 1000
    if isinstance(heat_density_map, np.ndarray):
        if not in_orig:
            raise TypeError('The raster origin is of None type!')
        gt = in_orig
        hdm_arr = heat_density_map
    elif isinstance(heat_density_map, str):
        hdm_arr, gt = RA(heat_density_map, return_gt=True)
    # division by 1000 for MWh to GWh
    total_heat_demand = np.sum(hdm_arr)/1000
    hdm_arr_filtered = hdm_arr * (hdm_arr > pix_threshold)
    DH_Selected_Region = DHRegions(hdm_arr_filtered, DH_threshold)
    hdm_dh_region_cut = hdm_arr*(DH_Selected_Region > 0).astype(int)
    # return DH_Selected_Region and raster geotransform array
    return DH_Selected_Region, hdm_dh_region_cut, gt, total_heat_demand
