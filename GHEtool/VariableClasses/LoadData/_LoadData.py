import abc
from abc import ABC
from typing import Union

import numpy as np

from GHEtool.VariableClasses.BaseClass import BaseClass


class _LoadData(BaseClass, ABC):
    """
    This class contains information w.r.t. load data for the borefield sizing.
    """

    AVG_UPM: float = 730.  # number of hours per month
    DEFAULT_LENGTH_PEAK: int = 6  # hours
    DEFAULT_SIMULATION_PERIOD: int = 20  # years

    def __init__(self, hourly_resolution: bool, simulation_period: int = DEFAULT_SIMULATION_PERIOD,
                 start_month: int = 1):
        """

        Parameters
        ----------
        hourly_resolution : bool
            True if the load class uses an hourly resolution
        simulation_period : int
            Length of the simulation period in years
        start_month : int
            Start month of the simulation (jan: 1, feb: 2 ...)
        """
        self.hourly_resolution: bool = hourly_resolution
        self.simulation_period: int = simulation_period
        self._peak_injection_duration: int = _LoadData.DEFAULT_LENGTH_PEAK
        self._peak_extraction_duration: int = _LoadData.DEFAULT_LENGTH_PEAK
        self.tm: int = _LoadData.AVG_UPM * 3600  # time in a month in seconds
        self._all_months_equal: bool = True  # true if it is assumed that all months are of the same length
        self._start_month: int = 1
        self.start_month = start_month

    @property
    def start_month(self) -> int:
        """
        This function returns the start month.

        Returns
        -------
        int
            Start month
        """
        return self._start_month

    @start_month.setter
    def start_month(self, month: int) -> None:
        """
        This function sets the start month.

        Parameters
        ----------
        month : int
            Start month (jan: 1, feb: 2 ...)

        Returns
        -------
        None

        Raises
        ----------
        ValueError
            When the start month is smaller than 1, larger than 12 or non-integer
        """

        if not isinstance(month, int) or month < 1 or month > 12:
            raise ValueError(f'The value for month is: {month} which is not an integer in [1,12].')

        self._start_month = month

    @abc.abstractmethod
    def correct_for_start_month(self, array: np.ndarray) -> np.ndarray:
        """
        This function corrects the load for the correct start month.
        If the simulation starts in september, the start month is 9 and hence the array should start
        at index 9.

        Parameters
        ----------
        array : np.ndarray
            Load array

        Returns
        -------
        load : np.ndarray
        """

    @property
    def all_months_equal(self) -> bool:
        """
        Returns the attribute all months are equal

        Returns
        -------
        bool
            True if the months are assumed to be of equal length (i.e. 730 hours/month).
            False if the correct number of hours is used.
        """
        return self._all_months_equal

    @all_months_equal.setter
    def all_months_equal(self, bool: bool) -> None:
        """
        Sets the all_months_equal attribute.

        Parameters
        ----------
        bool : bool
            True if the months are assumed to be of equal length (i.e. 730 hours/month).
            False if the correct number of hours is used.

        Returns
        -------
        None
        """
        self._all_months_equal = bool

    @property
    def UPM(self) -> np.ndarray:
        """
        Depending on whether all months are assumed to have equal length, the UPM are either constant
        or vary during the year.

        Returns
        -------
        Hours per month : np.ndarray
        """
        if self.all_months_equal:
            # every month has equal length
            return np.ones(12) * _LoadData.AVG_UPM
        else:
            return np.array([744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744])

    @abc.abstractmethod
    def _check_input(self, input: Union[np.ndarray, list, tuple]) -> bool:
        """
        This function checks whether the input is valid or not.

        Parameters
        ----------
        input : np.ndarray, list, tuple
            Thermal load input

        Returns
        -------
        bool
            True if the input is correct for the load class
        """

    @abc.abstractmethod
    def peak_extraction(self) -> np.ndarray:
        """
        This function returns the peak extraction in kW/month.

        Returns
        -------
        peak extraction : np.ndarray
        """

    @abc.abstractmethod
    def peak_injection(self) -> np.ndarray:
        """
        This function returns the peak injection in kW/month.

        Returns
        -------
        peak cooling : np.ndarray
        """

    @abc.abstractmethod
    def baseload_extraction(self) -> np.ndarray:
        """
        This function returns the baseload extraction in kWh/month.

        Returns
        -------
        baseload extraction : np.ndarray
        """

    @abc.abstractmethod
    def baseload_injection(self) -> np.ndarray:
        """
        This function returns the baseload injection in kWh/month.

        Returns
        -------
        baseload injection : np.ndarray
        """

    @property
    def _peak_extraction(self) -> np.ndarray:
        """
        This function returns the peak extraction, corrected for the start month in kW/month.

        Returns
        -------
        peak extraction : np.ndarray
        """
        return self.correct_for_start_month(self.peak_extraction)

    @property
    def _peak_injection(self) -> np.ndarray:
        """
        This function returns the peak injection, corrected for the start month in kW/month.

        Returns
        -------
        peak cooling : np.ndarray
        """
        return self.correct_for_start_month(self.peak_injection)

    @property
    def _baseload_extraction(self) -> np.ndarray:
        """
        This function returns the baseload extraction, corrected for the start month in kWh/month.

        Returns
        -------
        baseload extraction : np.ndarray
        """
        return self.correct_for_start_month(self.baseload_extraction)

    @property
    def _baseload_injection(self) -> np.ndarray:
        """
        This function returns the baseload injection, corrected for the start month in kWh/month.

        Returns
        -------
        baseload injection : np.ndarray
        """

        return self.correct_for_start_month(self.baseload_injection)

    @property
    def baseload_extraction_power(self) -> np.ndarray:
        """
        This function returns the baseload extraction in kW avg/month.

        Returns
        -------
        baseload extraction : np.ndarray
        """
        return np.divide(self._baseload_extraction, self.UPM)

    @property
    def baseload_injection_power(self) -> np.ndarray:
        """
        This function returns the baseload injection in kW avg/month.

        Returns
        -------
        baseload injection : np.ndarray
        """
        return np.divide(self._baseload_injection, self.UPM)

    @property
    def yearly_extraction_load(self) -> float:
        """
        This function returns the yearly extraction load in kWh/year.

        Returns
        -------
        float
            Yearly extraction load kWh/year
        """
        return np.sum(self.baseload_extraction)

    @property
    def yearly_injection_load(self) -> float:
        """
        This function returns the yearly injection load in kWh/year.

        Returns
        -------
        float
            Yearly injection load kWh/year
        """
        return np.sum(self.baseload_injection)

    @property
    def baseload_extraction_simulation_period(self) -> np.ndarray:
        """
        This function returns the baseload extraction in kWh/month for a whole simulation period.

        Returns
        -------
        baseload extraction : np.ndarray
            baseload extraction for the whole simulation period
        """
        return np.tile(self._baseload_extraction, self.simulation_period)

    @property
    def baseload_injection_simulation_period(self) -> np.ndarray:
        """
        This function returns the baseload injection in kWh/month for a whole simulation period.

        Returns
        -------
        baseload injection : np.ndarray
            baseload injection for the whole simulation period
        """
        return np.tile(self._baseload_injection, self.simulation_period)

    @property
    def peak_extraction_simulation_period(self) -> np.ndarray:
        """
        This function returns the peak extraction in kW/month for a whole simulation period.

        Returns
        -------
        peak extraction : np.ndarray
            peak extraction for the whole simulation period
        """
        return np.tile(self._peak_extraction, self.simulation_period)

    @property
    def peak_injection_simulation_period(self) -> np.ndarray:
        """
        This function returns the peak injection in kW/month for a whole simulation period.

        Returns
        -------
        peak injection : np.ndarray
            peak injection for the whole simulation period
        """
        return np.tile(self._peak_injection, self.simulation_period)

    @property
    def baseload_extraction_power_simulation_period(self) -> np.ndarray:
        """
        This function returns the average extraction power in kW avg/month for a whole simulation period.

        Returns
        -------
        average extraction power : np.ndarray
            average extraction power for the whole simulation period
        """
        return np.tile(self.baseload_extraction_power, self.simulation_period)

    @property
    def baseload_injection_power_simulation_period(self) -> np.ndarray:
        """
        This function returns the average injection power in kW avg/month for a whole simulation period.

        Returns
        -------
        average injection power : np.ndarray
            average injection for the whole simulation period
        """
        return np.tile(self.baseload_injection_power, self.simulation_period)

    @property
    def imbalance(self) -> float:
        """
        This function calculates the ground imbalance.
        A positive imbalance means that the field is injection dominated, i.e. it heats up every year.

        Returns
        -------
        imbalance : float
        """
        return self.yearly_injection_load - self.yearly_extraction_load

    @property
    def monthly_average_load(self) -> np.ndarray:
        """
        This function calculates the average monthly load in kW.

        Returns
        -------
        monthly average load : np.ndarray
        """
        return self.baseload_injection_power - self.baseload_extraction_power

    @property
    def monthly_average_load_simulation_period(self) -> np.ndarray:
        """
        This function calculates the average monthly load in kW for the whole simulation period.

        Returns
        -------
        monthly average load : np.ndarray
        """
        return np.tile(self.monthly_average_load, self.simulation_period)

    @property
    def peak_extraction_duration(self) -> float:
        """
        Length of the peak in extraction.

        Returns
        -------
        Length peak in extraction [s]
        """
        return self._peak_extraction_duration * 3600

    @peak_extraction_duration.setter
    def peak_extraction_duration(self, duration: float) -> None:
        """
        This function sets the duration of the peak in extraction.

        Parameters
        ----------
        duration : float
            Duration of the peak in hours

        Returns
        -------
        None
        """
        self._peak_extraction_duration = duration

    @property
    def peak_injection_duration(self) -> float:
        """
        Duration of the peak in injection.

        Returns
        -------
        Duration of the peak in injection [s]
        """
        return self._peak_injection_duration * 3600

    @peak_injection_duration.setter
    def peak_injection_duration(self, duration: float) -> None:
        """
        This function sets the duration of the peak in cooling.

        Parameters
        ----------
        duration : float
            Duration of the peak in hours

        Returns
        -------
        None
        """
        self._peak_injection_duration = duration

    @property
    def peak_duration(self) -> None:
        """
        Dummy object to set the length peak for both extraction and injection.

        Returns
        -------
        None
        """
        return

    @peak_duration.setter
    def peak_duration(self, duration: float) -> None:
        """
        This sets the duration of both the extraction and injection peak.

        Parameters
        ----------
        duration : float
            Duration in hours

        Returns
        -------
        None
        """
        self.peak_extraction_duration = duration
        self.peak_injection_duration = duration

    @property
    def ty(self) -> float:
        """
        Simulation period in seconds.

        Returns
        -------
        Simulation period in seconds
        """
        return self.simulation_period * 8760 * 3600

    @property
    def time_L3(self) -> np.ndarray:
        """
        Time for L3 sizing, i.e. an array with monthly the cumulative seconds that have passed.
        [744, 1416 ...] * 3600

        Returns
        -------
        Times for the L3 sizing : np.ndarray
        """
        return np.cumsum(np.tile(self.UPM, self.simulation_period) * 3600)

    @property
    def time_L4(self) -> np.ndarray:
        """
        Times for the L4 sizing, i.e. an array with hourly the cumulative seconds that have passed.
        [1, 2, 3, 4 ...] * 3600

        Returns
        -------
        Times for the L4 sizing : np.ndarray
        """
        # set the time constant for the L4 sizing
        time_L4 = 3600 * np.arange(1, 8760 * self.simulation_period + 1, dtype=np.float16)
        if np.isinf(time_L4).any():
            # 16 bit is not enough, go to 32
            time_L4 = 3600 * np.arange(1, 8760 * self.simulation_period + 1, dtype=np.float32)
        return time_L4

    @staticmethod
    def get_month_index(peak_load, avg_load) -> int:
        """
        This function calculates and returns the month index (i.e. the index of the month
        in which the field should be sized). It does so by taking 1) the month with the highest peak load.
        2) if all the peak loads are the same, it takes the month with the highest average load
        3) if all average loads are the same, it takes the last month

        Parameters
        ----------
        peak_load : np.ndarray
            array with the peak loads [kW]
        avg_load : np.ndarray
            array with the monthly average loads [kW]

        Returns
        -------
        month_index : int
            0 = jan, 1 = feb ...
        """
        # check if all peak loads are equal
        if not np.all(peak_load == peak_load[0]):
            return np.where(peak_load == np.max(peak_load))[0][-1]

        # if the average load is not constant, the month with the highest average load is chosen
        # if it is constant, the last month is returned
        return np.where(avg_load == np.max(avg_load))[0][-1]

    def _calculate_last_year_params(self, HC: bool) -> tuple:
        """
        This function calculates the parameters for the sizing based on the last year of operation.
        This is needed for the L2 sizing.

        Parameters
        ----------
        HC : bool
            True if the borefield is limited by extraction load

        Returns
        -------
        th, qh, qm, qa : float
            Peak length [s], peak load [W], corresponding monthly load [W], yearly imbalance [W]
        """

        # convert imbalance to Watt
        qa = self.imbalance / 8760. * 1000

        if HC:
            # limited by extraction load

            # set length peak
            th = self.peak_extraction_duration

            # Select month with the highest peak load and take both the peak and average load from that month
            month_index = self.get_month_index(self._peak_extraction, self.baseload_extraction_power)
            qm = self.monthly_average_load[month_index] * 1000.
            qh = self.max_peak_extraction * 1000.

            # correct signs
            qm = -qm
            qa = -qa

        else:
            # limited by injection load

            # set length peak
            th = self.peak_injection_duration

            # Select month with the highest peak load and take both the peak and average load from that month
            month_index = self.get_month_index(self._peak_injection, self.baseload_injection_power)
            qm = self.monthly_average_load[month_index] * 1000.
            qh = self.max_peak_injection * 1000.

        return th, qh, qm, qa

    def _calculate_first_year_params(self, HC: bool) -> tuple:
        """
        This function calculates the parameters for the sizing based on the first year of operation.
        This is needed for the L2 sizing.

        Parameters
        ----------
        HC : bool
            True if the borefield is limited by extraction load

        Returns
        -------
        th, tpm, tcm, qh, qpm, qcm : float
            Peak duration [s], cumulative time passed at the start of the month [s],
            cumulative time passed at the end of the month [s], peak load [W],
            average cumulative load of the past months [W avg],
            average load of the current month [W avg]
        """

        if HC:
            # limited by extraction load

            # set peak length
            th = self.peak_extraction_duration

            # Select month with the highest peak load and take both the peak and average load from that month
            month_index = self.get_month_index(self._peak_extraction, self.baseload_extraction_power)
            qh = self.max_peak_extraction * 1000.

            qm = self.monthly_average_load[month_index] * 1000.

            if month_index < 1:
                qpm = 0
            else:
                qpm = np.sum(self.monthly_average_load[:month_index]) * 1000 / (month_index + 1)

            qm = -qm
        else:
            # limited by injection

            # set peak length
            th = self.peak_injection_duration

            # Select month with the highest peak load and take both the peak and average load from that month
            month_index = self.get_month_index(self._peak_injection, self.baseload_injection_power)
            qh = self.max_peak_injection * 1000.

            qm = self.monthly_average_load[month_index] * 1000.
            if month_index < 1:
                qpm = 0
            else:
                qpm = np.sum(self.monthly_average_load[:month_index]) * 1000 / (month_index + 1)

        tcm = self.time_L3[month_index]
        tpm = self.time_L3[month_index - 1] if month_index > 0 else 0

        return th, tpm, tcm, qh, qpm, qm

    @property
    def max_peak_injection(self) -> float:
        """
        This returns the max peak injection in kW.

        Returns
        -------
        max peak cooling : float
        """
        return np.max(self.peak_injection)

    @property
    def max_peak_extraction(self) -> float:
        """
        This returns the max peak extraction in kW.

        Returns
        -------
        max peak heating : float
        """
        return np.max(self.peak_extraction)

