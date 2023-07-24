"""
This document contains the variable classes for the fluid data.
"""
from __future__ import annotations

from math import pi

import numpy as np
import pygfunction as gt

from GHEtool.VariableClasses.BaseClass import BaseClass


class FluidData(BaseClass):
    """
    Contains information regarding the fluid data of the borefield.
    """

    __slots__ = 'k_f', 'rho', 'Cp', 'mu', 'mfr'

    def __init__(self, mfr: float = None,
                 k_f: float = None,
                 rho: float = None,
                 Cp: float = None,
                 mu: float = None):
        """

        Parameters
        ----------
        mfr : float
            Mass flow rate per borehole [kg/s]
        k_f : float
            Thermal Conductivity of the fluid [W/mK]
        rho : float
            Density of the fluid [kg/m3]
        Cp : float
            Thermal capacity of the fluid [J/kgK]
        mu : float
            Dynamic viscosity of the fluid [Pa/s]
        """
        self.k_f: float | None = k_f  # Thermal conductivity W/mK
        self.mfr: float | None = mfr  # Mass flow rate per borehole kg/s
        self.rho: float | None = rho  # Density kg/m3
        self.Cp: float | None = Cp    # Thermal capacity J/kgK
        self.mu: float | None = mu    # Dynamic viscosity Pa/s

    def set_mass_flow_rate(self, mfr: float) -> None:
        """
        This function sets the mass flow rate per borehole.

        Parameters
        ----------
        mfr : fluid
            Mass flow rate per borehole [kg/s]

        Returns
        -------
        None
        """
        self.mfr = mfr

    def __eq__(self, other):
        if not isinstance(other, FluidData):
            return False
        for i in self.__slots__:
            if getattr(self, i) != getattr(other, i):
                return False
        return True
