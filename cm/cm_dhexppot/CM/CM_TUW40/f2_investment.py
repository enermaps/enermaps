import os
import sys
import numpy as np
from osgeo import gdal
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW0.rem_mk_dir import rm_file
from CM.CM_TUW1.read_raster import raster_array as RA
from CM.CM_TUW19 import run_cm as CM19


def annuity(r, period):
    period = int(period)
    r = float(r)
    if r == 0:
        return 1
    return ((1+r)**period - 1) / (r*(1+r)**period)


def calc_adjustment_factor(market_share):
    # term inside log should be in percent: obtained for 10 buildings in sparse areas
    market_share_in_percent = market_share * 100
    if market_share_in_percent < 20:
        market_share_in_percent = 20
    '''
    # old: adjustment factor for 20 buildings
    adjustment_factor = 0.4258 * np.log(market_share_in_percent) - 0.96089
    '''
    adjustment_factor = 0.604 * np.log(market_share_in_percent) - 1.7815
    if adjustment_factor > 1:
        adjustment_factor = 1
    return adjustment_factor


def dh_demand(P, OFP, dA_slope=0.0486, dA_intercept=0.0007, dataType='float32'):
    '''
    Important Note:
    1) Here, for the calculation of plot ratio, I used gross floor area raster
    in one hectar resolution (unit: m2). It should be divided by 1e4 to get the
    plot ratio.
    2) if you have plot ratio raster, remove the 1e4 factor.
    3) Distribution cost is calculated for those pixel that their corresponding
    pipe diameter is equal or greater than 0.
    the input heat density map should be in GWh/km2.
    '''
    horizon = int(P.last_year) - int(P.start_year) + 1
    horizon = int(horizon)
    if horizon > int(P.depreciation_period):
        horizon = P.depreciation_period
        remaining_years = 0
        reinvestment_factor = 1
    else:
        remaining_years = int(P.depreciation_period) - int(horizon)
        reinvestment_factor = 1 + remaining_years / P.depreciation_period
    hdm_st, geo_transform = RA(OFP.inRasterHDM_st, dType='float32', return_gt=True)
    hdm_end = RA(OFP.inRasterHDM_end, dType='float32')
    # gfa in hectar should be devided by 10000 to get right values for plot ratio (m2/m2).
    plotRatio = RA(OFP.inRasterGFA_st, dType='float32') / 10000
    row, col = np.nonzero((hdm_st > 0).astype(int) * (hdm_end > 0).astype(int) * (plotRatio > 0.0).astype(int))
    # unit conversion from MWh/ha to GJ/m2
    sparseDemand = 0.00036*hdm_st[row, col]
    PR_sparse = plotRatio[row, col]
    hdm_change_ratio_sparse = hdm_end[row, col] / hdm_st[row, col]
    energy_reduction_factor_sparse = hdm_change_ratio_sparse ** (1 / (horizon - 1))
    # the unit for L is m however in each m2
    # L is in m: to get the value for each pixel (ha) you should multiply it
    # by 10000 because 1 pixel has 10000 m2
    '''
    # The following formulation of L comes from Persson et al. 2019 paper with
    # the title "Heat Roadmap Europe: Heat distribution costs"
    L = 1 / ((PR_sparse <= 0.4).astype(int) * (137.5 * PR_sparse + 5) + (PR_sparse > 0.4).astype(int) * 60)
    '''
    adjustment_factor = calc_adjustment_factor(P.end_dh_connection_rate)
    # the following formula originates from D4.5 of the H2020 project sEEnergies
    pr_upper = (PR_sparse > np.exp(-2)).astype(int)
    pr_lower = (PR_sparse <= np.exp(-2)).astype(int)
    L = 1 / (pr_lower * np.exp(2) * adjustment_factor / PR_sparse + pr_upper * np.exp(4))
    L_servicePipes = 1 / (
            pr_lower * np.exp(2) * adjustment_factor / PR_sparse + pr_upper * np.exp(
                pr_upper * (np.log(PR_sparse) + 3.5) / (0.7737 + 0.18559 * np.log(PR_sparse))))
    # initialize the variables
    q = 0
    # q_new = P.st_dh_connection_rate * sparseDemand
    q_tot = np.copy(sparseDemand)
    q_max = np.zeros_like(q_tot)
    for i in range(horizon):
        q_tot = sparseDemand * energy_reduction_factor_sparse**i
        q_new = q_tot * (float(P.st_dh_connection_rate) + i * (
                    float(P.end_dh_connection_rate) - float(P.st_dh_connection_rate)) / (horizon - 1))
        # q_new is a non-zero sparse matrix. The development of demand can be
        # checked by comparing just one element of q_new with q_max.
        q_max = np.max((q_max, q_new), axis=0)
        q += q_new / (1 + float(P.interest))**i
    if remaining_years > 0:
        if P.interest > 0:
            # in the first year, connection rate st exists. so use horizon-1 for annuity.
            alpha_horizon = annuity(P.interest, horizon-1)
            alpha_depreciation = annuity(P.interest, P.depreciation_period)
            rest_annuity_factor = alpha_depreciation - alpha_horizon
            q = q + q_new * rest_annuity_factor
        else:
            q = q + q_new * remaining_years
    linearHeatDensity = q_max / L
    linearHeatDensity_servicePipes = q_max / L_servicePipes
    # this step is performed to avoid negative average pipe diameter
    LHD_THRESHOLD = -dA_intercept/dA_slope
    filtered_LHD = (np.log(linearHeatDensity) < LHD_THRESHOLD).astype(int)
    elements = np.nonzero(filtered_LHD)[0]
    dA = dA_slope * (np.log(linearHeatDensity)) + dA_intercept
    dA[elements] = 0
    dA_servicePipes = np.zeros_like(dA)
    # lower limit of linear heat densities at 1.5 GJ/m was set. Below this
    # threshold, pipe diameters of 0.02m were applied uniformly for all hectare
    # grid cells with present heat density values above zero.
    # Note: linearHeatDensity is calculated for cells with heat demand above zero
    dA[((linearHeatDensity < 1.5).astype(int) * (dA > 0).astype(int)).astype(bool)] = 0.02
    dA_servicePipes[((linearHeatDensity_servicePipes < 1.5).astype(int) * (dA > 0.02).astype(int)).astype(bool)] = 0.02
    dA_servicePipes[((linearHeatDensity_servicePipes >= 1.5).astype(int) * (dA > 0.03).astype(int)).astype(bool)] = 0.03
    dA_servicePipes[elements] = 0
    q_max[elements] = 0
    # absolute investment in EURO
    abs_investment_dist = 1e4 * L * (P.c1 + P.c2*dA)
    abs_investment_servicePipes = 1e4 * L_servicePipes * (P.c1 + P.c2*dA_servicePipes)
    abs_investment_total = abs_investment_dist + abs_investment_servicePipes
    abs_investment_dist[elements] = 0
    abs_investment_servicePipes[elements] = 0
    abs_investment_total[elements] = 0
    # investment in EUR/GJ
    investment_dist = 1e-4 * reinvestment_factor * abs_investment_dist / q
    investment_servicePipes = 1e-4 * reinvestment_factor * abs_investment_servicePipes / q
    investment = investment_dist + investment_servicePipes
    q[elements] = 0
    finalInvestment_dist = np.zeros_like(hdm_st, dtype=dataType)
    finalInvestment_servicePipes = np.zeros_like(hdm_st, dtype=dataType)
    # from Euro/GJ to Euro/MWh
    finalInvestment_dist[row, col] = investment_dist*3.6
    finalInvestment_servicePipes[row, col] = investment_servicePipes*3.6
    finalInvestment = np.zeros_like(hdm_st, dtype=dataType)
    # from Euro/GJ to Euro/MWh
    finalInvestment[row, col] = investment*3.6
    supplied_heat_during_investment_period = np.zeros_like(finalInvestment, dtype=dataType)
    maxDHdem_arr = np.zeros_like(finalInvestment, dtype=dataType)
    # DH demand density in MWh within the study horizon
    maxDHdem_arr[row, col] = q_max*10000/3.6
    supplied_heat_during_investment_period[row, col] = q * 10000 / 3.6
    invest_Euro_arr = np.zeros_like(finalInvestment, dtype=dataType)
    invest_Euro_arr[row, col] = abs_investment_total
    '''
    hdm_last_year = np.zeros_like(finalInvestment, dtype=dataType)
    # total demand in the last year of study horizon in MWh/ha
    hdm_last_year[row, col] = q_tot*10000/3.6
    '''
    # Length of distribution pipes (L)
    length_distribution_pipes = np.zeros_like(finalInvestment, dtype=dataType)
    length_distribution_pipes[row, col] = L
    length_distribution_pipes[row, col][elements] = 0
    
    length_service_pipes = np.zeros_like(finalInvestment, dtype=dataType)
    length_service_pipes[row, col] = L_servicePipes
    length_service_pipes[row, col][elements] = 0

    # Save raster files
    CM19.main(OFP.maxDHdem, geo_transform, dataType, maxDHdem_arr)
    CM19.main(OFP.supplied_heat_during_investment_period, geo_transform, dataType,
              supplied_heat_during_investment_period)
    CM19.main(OFP.invest_Euro, geo_transform, dataType, invest_Euro_arr)
    # CM19.main(OFP.hdm_cut_last_year, geo_transform, dataType, hdm_last_year)
    CM19.main(OFP.total_dist_pipe_length, geo_transform, dataType, length_distribution_pipes)
    CM19.main(OFP.total_serv_pipe_length, geo_transform, dataType, length_service_pipes)
    CM19.main(OFP.inv_dist, geo_transform, dataType, finalInvestment_dist)
    CM19.main(OFP.inv_service_pipe, geo_transform, dataType, finalInvestment_servicePipes)
    CM19.main(OFP.inv_sum, geo_transform, dataType, finalInvestment)
