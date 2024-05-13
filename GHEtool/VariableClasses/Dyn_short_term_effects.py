"""
This document contains the code to add the dynamic short-term effects to the pygfunction package as they can be
translated into short-term g-functions following the paper of (Meertens et al., 2023)

References:
-----------
    -
"""

import pygfunction as gt
import numpy as np

def radial_numerical_borehole(self,time, alpha):





def update_pygfunction() -> None:
    """
    This function updates pygfunction by adding the cylindrical correction methods to it.

    Returns
    -------
    None
    """
    gt.heat_transfer.cylindrical_heat_source = cylindrical_heat_source
    gt.heat_transfer.infinite_line_source = infinite_line_source
    gt.gfunction._Equivalent.thermal_response_factors = thermal_response_factors
    gt.gfunction._BaseSolver.solve = solve
    gt.gfunction._BaseSolver.__init__ = __init__