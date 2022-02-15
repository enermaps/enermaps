import os
import sys
import numpy as np
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW40.f2_investment import dh_demand
from CM.CM_TUW40.f3_coherent_areas import distribuition_costs


def main(P, OFP):
    # f2: calculate pixel based values
    dh_demand(P, OFP)
    # f3: Determination of coherent areas based on the distribution grid cost
    # ceiling and available capital for investment.
    distribuition_costs(P, OFP)
