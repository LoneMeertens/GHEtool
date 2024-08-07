import pytest

import numpy as np

from GHEtool.VariableClasses import MonthlyGeothermalLoadAbsolute, HourlyGeothermalLoad, MonthlyGeothermalLoadMultiYear
from GHEtool.Validation.cases import load_case


def test_checks():
    load = MonthlyGeothermalLoadAbsolute()
    assert not load._check_input(2)
    assert not load._check_input(np.ones(11))
    assert not load._check_input(-1*np.ones(12))
    assert load._check_input([1]*12)
    assert load._check_input(np.ones(12))


def test_start_month_general():
    load = MonthlyGeothermalLoadAbsolute()
    assert load.start_month == 1
    with pytest.raises(ValueError):
        load.start_month = 1.5
    with pytest.raises(ValueError):
        load.start_month = 0
    with pytest.raises(ValueError):
        load.start_month = 13
    load.start_month = 12
    assert load.start_month == 12
    load.start_month = 1
    assert load.start_month == 1


def test_imbalance():
    load = MonthlyGeothermalLoadAbsolute(np.ones(12)*10, np.ones(12), np.ones(12), np.ones(12))
    assert load.imbalance == -108
    load = MonthlyGeothermalLoadAbsolute(np.ones(12), np.ones(12) * 10, np.ones(12), np.ones(12))
    assert load.imbalance == 108


def test_baseload_heating():
    load = MonthlyGeothermalLoadAbsolute()
    assert np.array_equal(load.baseload_heating, np.zeros(12))
    load.baseload_heating = np.linspace(0, 11, 12)
    assert np.array_equal(load.baseload_heating, np.linspace(0, 11, 12))
    load.set_baseload_heating(np.linspace(1, 12, 12))
    assert np.array_equal(load.baseload_heating, np.linspace(1, 12, 12))
    assert np.array_equal(load.baseload_heating / 730, load.baseload_heating_power)
    assert np.array_equal(load.baseload_heating_power, load.peak_heating)
    with pytest.raises(ValueError):
        load.set_baseload_heating(np.ones(11))


def test_baseload_cooling():
    load = MonthlyGeothermalLoadAbsolute()
    assert np.array_equal(load.baseload_cooling, np.zeros(12))
    load.baseload_cooling = np.linspace(0, 11, 12)
    assert np.array_equal(load.baseload_cooling, np.linspace(0, 11, 12))
    load.set_baseload_cooling(np.linspace(1, 12, 12))
    assert np.array_equal(load.baseload_cooling, np.linspace(1, 12, 12))
    assert np.array_equal(load.baseload_cooling / 730, load.baseload_cooling_power)
    assert np.array_equal(load.baseload_cooling_power, load.peak_cooling)

    with pytest.raises(ValueError):
        load.set_baseload_cooling(np.ones(11))


def test_peak_heating():
    load = MonthlyGeothermalLoadAbsolute()
    assert np.array_equal(load.peak_heating, np.zeros(12))
    load.peak_heating = np.linspace(0, 11, 12)
    assert np.array_equal(load.peak_heating, np.linspace(0, 11, 12))
    load.set_peak_heating(np.linspace(1, 12, 12))
    assert np.array_equal(load.peak_heating, np.linspace(1, 12, 12))
    load.set_baseload_heating(np.ones(12) * 730 * 5)
    assert np.array_equal(load.peak_heating, np.array([5., 5., 5., 5., 5., 6., 7., 8., 9., 10., 11., 12.]))
    with pytest.raises(ValueError):
        load.set_peak_heating(np.ones(11))


def test_peak_cooling():
    load = MonthlyGeothermalLoadAbsolute()
    assert np.array_equal(load.peak_cooling, np.zeros(12))
    load.peak_cooling = np.linspace(0, 11, 12)
    assert np.array_equal(load.peak_cooling, np.linspace(0, 11, 12))
    load.set_peak_cooling(np.linspace(1, 12, 12))
    assert np.array_equal(load.peak_cooling, np.linspace(1, 12, 12))
    load.set_baseload_cooling(np.ones(12) * 730 * 5)
    assert np.array_equal(load.peak_cooling, np.array([5.,  5.,  5.,  5.,  5.,  6.,  7.,  8.,  9., 10., 11., 12.]))
    with pytest.raises(ValueError):
        load.set_peak_cooling(np.ones(11))


def test_times():
    load = MonthlyGeothermalLoadAbsolute()
    load.peak_cooling_duration = 6
    load.peak_heating_duration = 7
    assert load.peak_heating_duration == 7 * 3600
    assert load.peak_cooling_duration == 6 * 3600
    load.peak_duration = 8
    assert load.peak_heating_duration == 8 * 3600
    assert load.peak_cooling_duration == 8 * 3600

    load.simulation_period = 20
    assert load.time_L3[-1] == 20 * 3600 * 8760
    assert load.time_L4[-1] == 20 * 3600 * 8760

    load.simulation_period = 100
    assert not np.isinf(load.time_L4.any())
    assert load.ty == 100 * 8760 * 3600


def test_monthly_average_load():
    load = MonthlyGeothermalLoadAbsolute()
    load.baseload_cooling = np.ones(12) * 400
    load.baseload_heating = np.ones(12) * 500

    assert np.isclose(np.average(load.baseload_cooling_power) * 8760, 400 * 12)
    assert np.isclose(np.average(load.baseload_heating_power) * 8760, 500 * 12)
    assert np.array_equal(load.baseload_cooling_power, load.peak_cooling)
    assert np.array_equal(load.baseload_heating_power, load.peak_heating)

    assert np.array_equal(load.baseload_cooling_power_simulation_period,
                          np.tile(load.baseload_cooling_power, 20))
    assert np.array_equal(load.baseload_heating_power_simulation_period,
                          np.tile(load.baseload_heating_power, 20))
    assert np.array_equal(load.peak_heating_simulation_period,
                          np.tile(load.peak_heating, 20))
    assert np.array_equal(load.peak_cooling_simulation_period,
                          np.tile(load.peak_cooling, 20))
    assert np.array_equal(load.baseload_cooling_simulation_period,
                   np.tile(load.baseload_cooling, 20))
    assert np.array_equal(load.baseload_heating_simulation_period,
                          np.tile(load.baseload_heating, 20))

    assert np.array_equal(load.monthly_average_load, load.baseload_cooling_power-load.baseload_heating_power)
    assert np.array_equal(load.monthly_average_load_simulation_period,
                          load.baseload_cooling_power_simulation_period-load.baseload_heating_power_simulation_period)

    # test now with different month loads
    temp_cooling = load.baseload_cooling_power
    temp_heating = load.baseload_heating_power

    load.all_months_equal = False
    assert not np.array_equal(load.baseload_cooling_power, temp_cooling)
    assert not np.array_equal(load.baseload_heating_power, temp_heating)

    assert np.isclose(np.sum(np.multiply(load.baseload_cooling_power, load.UPM)), 400 * 12)
    assert np.isclose(np.sum(np.multiply(load.baseload_heating_power, load.UPM)), 500 * 12)


def test_params_last_year():
    load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    assert np.array_equal(load._calculate_last_year_params(False),
                          (21600.0, 240000.0, 65753.42465753425, 9132.420091324202))
    assert np.array_equal(load._calculate_last_year_params(True),
                          (21600.0, 160000.0, 25753.424657534248, -9132.420091324202))
    load.peak_heating = np.ones(12) * 160
    load.peak_cooling = np.ones(12) * 240
    assert np.array_equal(load._calculate_last_year_params(False),
                          (21600.0, 240000.0, 65753.42465753425, 9132.420091324202))
    assert np.array_equal(load._calculate_last_year_params(True),
                          (21600.0, 160000.0, 25753.424657534248, -9132.420091324202))


def test_params_first_year():
    load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    assert np.array_equal(load._calculate_first_year_params(False),
                          (21600.0, 18396000.0, 21024000.0, 240000.0, 6410.9589041095915, 65753.42465753425))
    assert np.array_equal(load._calculate_first_year_params(True),
                          (21600.0, 0, 2628000.0, 160000.0, 0, 25753.424657534248))
    temp = load.peak_cooling
    temp[0] = 250
    load.peak_cooling = temp
    assert np.array_equal(load._calculate_first_year_params(False),
                          (21600, 0, 2628000, 250000.0, 0, -25753.424657534248))

    load.peak_heating = np.ones(12) * 160
    load.peak_cooling = np.ones(12) * 240

    assert np.array_equal(load._calculate_first_year_params(False),
                          (21600, 18396000.0, 21024000.0, 240000.0, 6410.9589041095915, 65753.42465753425))
    assert np.array_equal(load._calculate_first_year_params(True),
                          (21600.0, 0, 2628000.0, 160000.0, 0, 25753.424657534248))


def test_get_month_index():
    load = MonthlyGeothermalLoadAbsolute()
    test_equal = np.array([2]*12)
    test_unequal = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10])
    test_unequal_2 = np.array([2]*12)
    test_unequal_2[3] = 30
    test_unequal_2[4] = 30

    assert load.get_month_index(test_equal, test_equal) == 11
    assert load.get_month_index(test_unequal, test_equal) == 10
    assert load.get_month_index(test_unequal, test_unequal) == 10
    assert load.get_month_index(test_equal, test_unequal) == 10
    assert load.get_month_index(test_equal, test_unequal_2) == 4


def test_dummy_peak_duration():
    test = MonthlyGeothermalLoadAbsolute()
    assert None is test.peak_duration


def test_dhw():
    load = MonthlyGeothermalLoadAbsolute()
    assert load.dhw == 0.
    load.add_dhw(1000)
    assert load.dhw == 1000.
    assert np.isclose(load.dhw_power, 1000./8760)
    load.dhw = 200
    assert load.dhw == 200.
    with pytest.raises(ValueError):
        load.add_dhw('test')
    with pytest.raises(ValueError):
        load.add_dhw(-10)

    load.dhw = 8760*10
    assert np.array_equal(np.full(12, 10), load.peak_heating)
    assert load.max_peak_heating == 10
    assert np.array_equal(np.full(12, 8760*10/12), load.baseload_heating)
    assert load.imbalance == -8760*10
    load.all_months_equal = False
    assert np.array_equal(np.array([7440., 6720., 7440., 7200., 7440., 7200., 7440., 7440., 7200., 7440., 7200., 7440.]), load.baseload_heating)


def test_dhw_exclude():
    load = MonthlyGeothermalLoadAbsolute()
    load.dhw = 8760*10
    assert np.array_equal(np.full(12, 10), load.peak_heating)
    load.exclude_DHW_from_peak = True
    assert load.dhw_power == 0
    assert np.array_equal(np.full(12, 10), load.peak_heating)  # since baseload

    load.peak_heating = [20]*12
    assert np.array_equal(np.full(12, 20), load.peak_heating)
    load.exclude_DHW_from_peak = False
    assert np.array_equal(np.full(12, 30), load.peak_heating)


def test_yearly_heating_cooling():
    load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    assert load.yearly_heating_load == 160000
    assert load.yearly_cooling_load == 240000


def test_eq():
    load_1 = MonthlyGeothermalLoadAbsolute(*load_case(2))
    load_2 = MonthlyGeothermalLoadAbsolute(*load_case(2))


    assert load_1 == load_2
    load_2.simulation_period = 55
    assert load_1 != load_2

    load_1.simulation_period = 55
    assert load_1 == load_2
    load_1.baseload_cooling = [i + 1 for i in load_1.baseload_cooling]

    assert load_1 != load_2
    load_2.baseload_cooling = [i + 1 for i in load_2.baseload_cooling]
    assert load_1 == load_2

    load_1.simulation_period = 55
    assert load_1 == load_2
    load_1.baseload_heating = [i + 1 for i in load_1.baseload_heating]

    assert load_1 != load_2
    load_2.baseload_heating = [i + 1 for i in load_2.baseload_heating]
    assert load_1 == load_2

    load_1.simulation_period = 55
    assert load_1 == load_2
    load_1.peak_heating = [i + 1 for i in load_1.peak_heating]

    assert load_1 != load_2
    load_2.peak_heating = [i + 1 for i in load_2.peak_heating]
    assert load_1 == load_2

    load_1.simulation_period = 55
    assert load_1 == load_2
    load_1.peak_cooling = [i + 1 for i in load_1.peak_cooling]

    assert load_1 != load_2
    load_2.peak_cooling = [i + 1 for i in load_2.peak_cooling]
    assert load_1 == load_2

    load_2 = HourlyGeothermalLoad()
    assert load_1 != load_2


def test_add():
    load_1 = MonthlyGeothermalLoadAbsolute(*load_case(2))
    load_2 = MonthlyGeothermalLoadAbsolute(*load_case(1))
    load_1.dhw = 10000
    load_2.dhw = 50000
    load_1.simulation_period = 20
    load_2.simulation_period = 30

    with pytest.raises(TypeError):
        load_1 + 55

    with pytest.warns():
        result = load_1 + load_2

    assert result.simulation_period == 30
    assert result.dhw == 60000
    assert np.allclose(result.baseload_heating, load_1.baseload_heating + load_2.baseload_heating)
    assert np.allclose(result.baseload_cooling, load_1.baseload_cooling + load_2.baseload_cooling)
    assert np.allclose(result._peak_heating, load_1._peak_heating + load_2._peak_heating)
    assert np.allclose(result._peak_cooling, load_1._peak_cooling + load_2._peak_cooling)

    load_2.simulation_period = 20
    load_2.peak_heating_duration = 18

    with pytest.warns():
        result = load_1 + load_2
        assert result.peak_heating_duration == 18*3600
    load_1.peak_heating_duration = 18
    try:
        with pytest.warns():
            result = load_1 + load_2
        assert False  # pragma: no cover
    except:
        assert True

    load_1.peak_cooling_duration = 18
    with pytest.warns():
        result = load_1 + load_2
        assert result.peak_cooling_duration == 18*3600
    load_2.peak_cooling_duration = 18
    try:
        with pytest.warns():
            result = load_1 + load_2
        assert False  # pragma: no cover
    except:
        assert True

    # add hourly load
    load_hourly = HourlyGeothermalLoad(np.full(8760, 10), np.full(8760, 20), 30, 10000)

    with pytest.warns():
        result = load_1 + load_hourly  # simulation period not equal

    assert result.simulation_period == 30
    assert result.dhw == 20000
    assert np.allclose(result._baseload_heating, load_1._baseload_heating + load_hourly.resample_to_monthly(load_hourly._hourly_heating_load)[1])
    assert np.allclose(result._baseload_cooling, load_1._baseload_cooling + load_hourly.resample_to_monthly(load_hourly._hourly_cooling_load)[1])
    assert np.allclose(result._peak_heating, load_1._peak_heating + load_hourly.resample_to_monthly(load_hourly._hourly_heating_load)[0])
    assert np.allclose(result._peak_cooling, load_1._peak_cooling + load_hourly.resample_to_monthly(load_hourly._hourly_cooling_load)[0])

    load_hourly.simulation_period = 20
    with pytest.warns():
        result = load_1 + load_hourly


def test_different_start_month():
    load = MonthlyGeothermalLoadAbsolute(baseload_heating=np.arange(1, 13, 1),
                                         baseload_cooling=np.arange(1, 13, 1),
                                         peak_cooling=np.arange(1, 13, 1),
                                         peak_heating=np.arange(1, 13, 1))
    load.start_month = 2
    result = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1])
    assert np.array_equal(load.baseload_heating, result)
    assert np.array_equal(load.baseload_cooling, result)
    assert np.array_equal(load.peak_heating, result)
    assert np.array_equal(load.peak_cooling, result)


def test_yearly_loads():
    load = MonthlyGeothermalLoadAbsolute(*load_case(2))
    load.simulation_period = 10
    assert np.array_equal(load.yearly_cooling_load_simulation_period, [240000]*10)
    assert np.array_equal(load.yearly_heating_load_simulation_period, [160000]*10)
    assert np.array_equal(load.yearly_cooling_peak_simulation_period, [240]*10)
    assert np.array_equal(load.yearly_heating_peak_simulation_period, [160]*10)


### continue for multi year
def test_checks_multiyear_monthly():
    load = MonthlyGeothermalLoadMultiYear()
    assert not load._check_input(2)
    assert not load._check_input(np.ones(11))
    assert not load._check_input(-1*np.ones(12*2))
    assert load._check_input([1]*12*2)
    assert load._check_input(np.ones(12))
    assert load._check_input(np.ones(12 * 3))
    assert not load._check_input(np.ones(30))
    with pytest.raises(ValueError):
        load.baseload_heating = np.ones(13)
    with pytest.raises(ValueError):
        load.baseload_cooling = np.ones(13)

