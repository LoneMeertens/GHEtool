"""
This document contains all the method data used in the test_methods document.
"""
import numpy as np
import pygfunction as gt

from GHEtool.test.methods.TestMethodClass import *
from GHEtool import *
from GHEtool.Validation.cases import load_case
from GHEtool.VariableClasses.BaseClass import UnsolvableDueToTemperatureGradient, MaximumNumberOfIterations

list_of_test_objects = TestMethodClass()

# Case 1 from main_functionalities
data = GroundConstantTemperature(3, 10)
peak_injection = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])
peak_extraction = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])
annual_extraction_load = 300 * 10 ** 3
annual_injection_load = 160 * 10 ** 3
monthly_load_extraction_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
monthly_load_injection_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
monthly_load_extraction = annual_extraction_load * monthly_load_extraction_percentage
monthly_load_injection = annual_injection_load * monthly_load_injection_percentage
borefield = Borefield(peak_extraction=peak_extraction, peak_injection=peak_injection,
                      baseload_extraction=monthly_load_extraction, baseload_injection=monthly_load_injection)
borefield.Rb = 0.2
borefield.set_ground_parameters(data)
borefield.create_rectangular_borefield(10, 12, 6, 6, 100, 4, 0.075)
borefield.set_max_avg_fluid_temperature(16)
borefield.set_min_avg_fluid_temperature(0)

list_of_test_objects.add(SizingObject(borefield, L2_output=92.07, L3_output=91.99, quadrant=1,
                                      name='Main functionalities (1)'))

fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
pipe_data = DoubleUTube(1, 0.015, 0.02, 0.4, 0.05)
borefield.set_fluid_parameters(fluid_data)
borefield.set_pipe_parameters(pipe_data)
borefield.calculation_setup(use_constant_Rb=False)

list_of_test_objects.add(SizingObject(borefield, L2_output=52.7, L3_output=52.73, quadrant=1,
                                      name='Main functionalities (2)'))
borefield.calculation_setup(atol=False)
list_of_test_objects.add(SizingObject(borefield, L2_output=52.716, L3_output=52.741, quadrant=1,
                                      name='Main functionalities (2), no atol'))

borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 110, 1, 0.075)
borefield = Borefield()
borefield.set_ground_parameters(data)
borefield.Rb = 0.12
borefield.set_borefield(borefield_gt)
hourly_load = HourlyGeothermalLoad()
hourly_load.load_hourly_profile(FOLDER.joinpath("test/methods/hourly_data/hourly_profile.csv"), header=True,
                                separator=";", col_extraction=0, col_injection=1)
borefield.load = hourly_load

list_of_test_objects.add(SizingObject(borefield, L2_output=182.73, L3_output=182.656, L4_output=182.337, quadrant=1,
                                      name='Hourly profile (1)'))

peak_injection = np.array([0., 0, 3.4, 6.9, 13., 18., 21., 50., 16., 3.7, 0., 0.])  # Peak injection in kW
peak_extraction = np.array([60., 42., 10., 5., 0., 0., 0., 0., 4.4, 8.5, 19., 36.])  # Peak extraction in kW
annual_extraction_load = 30 * 10 ** 3  # kWh
annual_injection_load = 16 * 10 ** 3  # kWh
monthly_load_extraction_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
monthly_load_injection_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
monthly_load_extraction = annual_extraction_load * monthly_load_extraction_percentage  # kWh
monthly_load_injection = annual_injection_load * monthly_load_injection_percentage  # kWh
borefield = Borefield(peak_extraction=peak_extraction, peak_injection=peak_injection,
                      baseload_extraction=monthly_load_extraction, baseload_injection=monthly_load_injection)
borefield.set_ground_parameters(data)
borefield.Rb = 0.2
borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
borefield.set_min_avg_fluid_temperature(0)  # minimum temperature
custom_field = gt.boreholes.L_shaped_field(N_1=4, N_2=5, B_1=5., B_2=5., H=100., D=4, r_b=0.05)
borefield.set_borefield(custom_field)

list_of_test_objects.add(SizingObject(borefield, L2_output=305.176, L3_output=306.898, quadrant=1,
                                      name='Custom config (1)'))

borefield_gt = gt.boreholes.rectangle_field(11, 11, 6, 6, 110, 1, 0.075)
peak_injection = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak injection in kW
peak_extraction = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])  # Peak extraction in kW
annual_extraction_load = 150 * 10 ** 3  # kWh
annual_injection_load = 400 * 10 ** 3  # kWh
monthly_load_extraction_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
monthly_load_injection_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])
monthly_load_extraction = annual_extraction_load * monthly_load_extraction_percentage  # kWh
monthly_load_injection = annual_injection_load * monthly_load_injection_percentage  # kWh
borefield = Borefield(peak_extraction=peak_extraction, peak_injection=peak_injection,
                      baseload_extraction=monthly_load_extraction, baseload_injection=monthly_load_injection)
borefield.set_ground_parameters(data)
borefield.set_borefield(borefield_gt)
borefield.Rb = 0.2
borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
borefield.set_min_avg_fluid_temperature(0)  # minimum temperature

list_of_test_objects.add(SizingObject(borefield, L2_output=190.223, L3_output=195.939, quadrant=2,
                                      name='Effect of borehole configuration (1)'))

borefield_gt = gt.boreholes.rectangle_field(6, 20, 6, 6, 110, 1, 0.075)
borefield.set_borefield(borefield_gt)

list_of_test_objects.add(SizingObject(borefield, L2_output=186.5208, L3_output=191.196, quadrant=2,
                                      name='Effect of borehole configuration (2)'))

data = GroundConstantTemperature(3.5, 10)
borefield_gt = gt.boreholes.rectangle_field(10, 12, 6.5, 6.5, 110, 4, 0.075)
correct_answers_L2 = (56.75, 117.223, 66.94, 91.266)
correct_answers_L3 = (56.771, 118.738, 66.471, 91.240)
for i in (1, 2, 3, 4):
    load = MonthlyGeothermalLoadAbsolute(*load_case(i))
    borefield = Borefield(load=load)
    borefield.set_ground_parameters(data)
    borefield.set_borefield(borefield_gt)
    borefield.Rb = 0.2
    borefield.set_max_avg_fluid_temperature(16)
    borefield.set_min_avg_fluid_temperature(0)
    list_of_test_objects.add(SizingObject(borefield, L2_output=correct_answers_L2[i - 1],
                                          L3_output=correct_answers_L3[i - 1], quadrant=i, name=f'BS2021 case {i}'))

correct_answers_L2 = (56.749, 117.223, 66.941, 91.266)
correct_answers_L3 = (56.770, 118.738, 66.471, 91.240)
customField = gt.boreholes.rectangle_field(N_1=12, N_2=10, B_1=6.5, B_2=6.5, H=110., D=4, r_b=0.075)
for i in (1, 2, 3, 4):
    load = MonthlyGeothermalLoadAbsolute(*load_case(i))
    borefield = Borefield(load=load)
    borefield.set_ground_parameters(data)
    borefield.set_borefield(customField)
    borefield.Rb = 0.2

    borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
    borefield.set_min_avg_fluid_temperature(0)  # minimum temperature
    list_of_test_objects.add(SizingObject(borefield, L2_output=correct_answers_L2[i - 1],
                                          L3_output=correct_answers_L3[i - 1], quadrant=i,
                                          name=f'Custom field case {i}'))

data = GroundConstantTemperature(3, 10)
borefield = Borefield()
borefield.set_ground_parameters(data)
borefield.Rb = 0.12
borefield.create_rectangular_borefield(10, 10, 6, 6, 110, 1, 0.075)
hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\hourly_profile.csv"), header=True,
                                separator=";",
                                col_extraction=0, col_injection=1)
borefield.load = hourly_load
borefield.simulation_period = 100
list_of_test_objects.add(SizingObject(borefield, L2_output=285.476, L3_output=288.541, L4_output=266.696, quadrant=4,
                                      name=f'Sizing method comparison (Validation)'))

ground_data = GroundFluxTemperature(3, 10)
fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
pipe_data = DoubleUTube(1, 0.015, 0.02, 0.4, 0.05)
borefield = Borefield()
borefield.create_rectangular_borefield(5, 4, 6, 6, 110, 4, 0.075)
borefield.set_ground_parameters(ground_data)
borefield.set_fluid_parameters(fluid_data)
borefield.set_pipe_parameters(pipe_data)
borefield.calculation_setup(use_constant_Rb=False)
borefield.set_max_avg_fluid_temperature(17)
borefield.set_min_avg_fluid_temperature(3)
hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\\auditorium.csv"), header=True, separator=";",
                                col_injection=0, col_extraction=1)
borefield.load = hourly_load
list_of_test_objects.add(SizingObject(borefield, L2_output=136.780, L3_output=136.294, L4_output=101.285, quadrant=1,
                                      name='BS2023 Auditorium'))
borefield.calculation_setup(max_nb_of_iterations=2)
list_of_test_objects.add(SizingObject(borefield, error_L2=MaximumNumberOfIterations, error_L3=MaximumNumberOfIterations,
                                      error_L4=MaximumNumberOfIterations, quadrant=1,
                                      name='BS2023 Auditorium (max nb of iter)'))
borefield.calculation_setup(atol=False, max_nb_of_iterations=40)
list_of_test_objects.add(SizingObject(borefield, L2_output=136.0488, L3_output=135.591, L4_output=101.061, quadrant=1,
                                      name='BS2023 Auditorium (no atol)'))
borefield.calculation_setup(force_deep_sizing=True)
list_of_test_objects.add(SizingObject(borefield, L2_output=136.0488, L3_output=135.477, L4_output=100.998, quadrant=1,
                                      name='BS2023 Auditorium (no atol, deep)'))
borefield.calculation_setup(force_deep_sizing=False)
borefield = Borefield()
borefield.create_rectangular_borefield(10, 10, 6, 6, 110, 4, 0.075)
borefield.set_ground_parameters(ground_data)
borefield.set_fluid_parameters(fluid_data)
borefield.set_pipe_parameters(pipe_data)
borefield.calculation_setup(use_constant_Rb=False)
borefield.set_max_avg_fluid_temperature(17)
borefield.set_min_avg_fluid_temperature(3)
hourly_load.simulation_period = 20
hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\office.csv"), header=True, separator=";",
                                col_injection=0, col_extraction=1)
borefield.load = hourly_load
list_of_test_objects.add(
    SizingObject(borefield, L2_output=111.180, L3_output=113.069, L4_output=107.08131844420905, quadrant=2,
                 name='BS2023 Office'))
borefield.calculation_setup(max_nb_of_iterations=5)
list_of_test_objects.add(SizingObject(borefield, error_L2=MaximumNumberOfIterations, error_L3=MaximumNumberOfIterations,
                                      error_L4=MaximumNumberOfIterations, quadrant=2,
                                      name='BS2023 Office (max nb of iter)'))
borefield.calculation_setup(deep_sizing=True)
list_of_test_objects.add(SizingObject(borefield, error_L2=MaximumNumberOfIterations, error_L3=MaximumNumberOfIterations,
                                      error_L4=MaximumNumberOfIterations, quadrant=2,
                                      name='BS2023 Office (max nb of iter, deep sizing)'))
borefield.calculation_setup(atol=False, max_nb_of_iterations=40)
list_of_test_objects.add(SizingObject(borefield, L2_output=110.845, L3_output=112.914, L4_output=106.920, quadrant=2,
                                      name='BS2023 Office (no atol)'))
borefield.calculation_setup(force_deep_sizing=True)
list_of_test_objects.add(SizingObject(borefield, L2_output=110.845, L3_output=112.720, L4_output=106.862, quadrant=2,
                                      name='BS2023 Office (no atol, deep)'))
borefield.calculation_setup(force_deep_sizing=False)

borefield.ground_data.Tg = 12
list_of_test_objects.add(
    SizingObject(borefield, error_L2=UnsolvableDueToTemperatureGradient, error_L3=UnsolvableDueToTemperatureGradient,
                 error_L4=UnsolvableDueToTemperatureGradient, quadrant=2,
                 name='BS2023 Office (unsolvable)'))
borefield.ground_data.Tg = 10

borefield = Borefield()
borefield.create_rectangular_borefield(15, 20, 6, 6, 110, 4, 0.075)
borefield.set_ground_parameters(ground_data)
borefield.set_fluid_parameters(fluid_data)
borefield.set_pipe_parameters(pipe_data)
borefield.calculation_setup(use_constant_Rb=False)
borefield.set_max_avg_fluid_temperature(17)
borefield.set_min_avg_fluid_temperature(3)
hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\swimming_pool.csv"), header=True,
                                separator=";",
                                col_injection=0, col_extraction=1)
borefield.load = hourly_load
list_of_test_objects.add(SizingObject(borefield, L2_output=305.509, L3_output=310.725, L4_output=308.269, quadrant=4,
                                      name='BS2023 Swimming pool'))
borefield.calculation_setup(atol=False, max_nb_of_iterations=40)
list_of_test_objects.add(SizingObject(borefield, L2_output=305.552, L3_output=310.746, L4_output=308.295, quadrant=4,
                                      name='BS2023 Swimming pool (no atol)'))
borefield.calculation_setup(force_deep_sizing=True)
# we expect the same values as hereabove, since quadrant 4 is limiting
list_of_test_objects.add(SizingObject(borefield, L2_output=305.552, L3_output=310.746, L4_output=308.295, quadrant=4,
                                      name='BS2023 Swimming pool (no atol, deep)'))
borefield.calculation_setup(force_deep_sizing=False)

ground_data_IKC = GroundFluxTemperature(2.3, 10.5, flux=2.85)
fluid_data_IKC = FluidData(0.2, 0.5, 1021.7, 3919, 0.0033)
pipe_data_IKC = SingleUTube(2.3, 0.016, 0.02, 0.42, 0.04)
monthly_injection = np.array([0, 0, 740, 1850, 3700, 7400, 7400, 7400, 5550, 2220, 740, 0]) * (1 + 1 / 4.86)
monthly_extraction = np.array([20064, 17784, 16644, 13680, 0, 0, 0, 0, 0, 12540, 15618, 17670]) * (1 - 1 / 4.49)
peak_injection = np.array([61] * 12) * (1 + 1 / 4.86)
peak_extraction = np.array([57] * 12) * (1 - 1 / 4.49)
load = MonthlyGeothermalLoadAbsolute(monthly_extraction, monthly_injection, peak_extraction, peak_injection, 25)
borefield = Borefield(load=load)
borefield.create_rectangular_borefield(4, 5, 8, 8, 110, 0.8, 0.07)
borefield.set_ground_parameters(ground_data_IKC)
borefield.set_fluid_parameters(fluid_data_IKC)
borefield.set_pipe_parameters(pipe_data_IKC)
borefield.calculation_setup(use_constant_Rb=False)
borefield.load.peak_duration = 10
borefield.set_max_avg_fluid_temperature(25)
borefield.set_min_avg_fluid_temperature(0)
list_of_test_objects.add(
    SizingObject(borefield, error_L2=UnsolvableDueToTemperatureGradient, error_L3=UnsolvableDueToTemperatureGradient,
                 name='Real case 1 (Error)'))
borefield.calculation_setup(max_nb_of_iterations=20)
list_of_test_objects.add(SizingObject(borefield, error_L2=RuntimeError, error_L3=UnsolvableDueToTemperatureGradient,
                                      name='Real case 1 (Error, max nb of iter)'))

ground_data_IKC = GroundFluxTemperature(2.3, 10.5, flux=2.3 * 2.85 / 100)
borefield.set_ground_parameters(ground_data_IKC)
borefield.calculation_setup(max_nb_of_iterations=40)
list_of_test_objects.add(SizingObject(borefield, L2_output=74.46, L3_output=74.866, quadrant=4,
                                      name='Real case 1 (Correct)'))
borefield.calculation_setup(atol=False)
list_of_test_objects.add(SizingObject(borefield, L2_output=74.46, L3_output=74.888, quadrant=4,
                                      name='Real case 1 (Correct) (no atol)'))
borefield.calculation_setup(atol=0.05)
borefield.set_ground_parameters(ground_data_IKC)
borefield.create_rectangular_borefield(2, 10, 8, 8, 60, 0.8, 0.07)
list_of_test_objects.add(SizingObject(borefield, L2_output=71.65, L3_output=72.054, quadrant=4,
                                      name='Real case 2 (Correct)'))

peakCooling = [0] * 12
peakHeating = [160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.]  # Peak extraction in kW
annualHeatingLoad = 300 * 10 ** 3  # kWh
monthlyLoadHeatingPercentage = [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144]
monthlyLoadHeating = list(map(lambda x: x * annualHeatingLoad, monthlyLoadHeatingPercentage))  # kWh
monthlyLoadCooling = [0] * 12  # kWh
borefield = Borefield(peak_extraction=peakHeating, peak_injection=peakCooling,
                      baseload_extraction=monthlyLoadHeating, baseload_injection=monthlyLoadCooling)
borefield.set_ground_parameters(data)
borefield.create_rectangular_borefield(10, 12, 6, 6, 110, 4, 0.075)
borefield.set_max_avg_fluid_temperature(16)
borefield.set_min_avg_fluid_temperature(0)
list_of_test_objects.add(SizingObject(borefield, L2_output=81.205, L3_output=82.077, quadrant=4,
                                      name='No injection L2/L3'))

peakCooling = [0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.]  # Peak injection in kW
peakHeating = [0] * 12
annualCoolingLoad = 160 * 10 ** 3  # kWh
monthlyLoadCoolingPercentage = [0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025]
monthlyLoadHeating = [0] * 12  # kWh
monthlyLoadCooling = list(map(lambda x: x * annualCoolingLoad, monthlyLoadCoolingPercentage))  # kWh
borefield = Borefield(peak_extraction=peakHeating, peak_injection=peakCooling,
                      baseload_extraction=monthlyLoadHeating, baseload_injection=monthlyLoadCooling)
borefield.set_ground_parameters(data)
borefield.create_rectangular_borefield(10, 12, 6, 6, 110, 4, 0.075)
borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
borefield.set_min_avg_fluid_temperature(0)  # minimum temperature
list_of_test_objects.add(SizingObject(borefield, L2_output=120.913, L3_output=123.346, quadrant=2,
                                      name='No extraction L2/L3'))
borefield = Borefield()
borefield.set_ground_parameters(data)
borefield.create_rectangular_borefield(10, 12, 6, 6, 110, 4, 0.075)
hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\hourly_profile.csv"))
borefield.load = hourly_load
borefield.load.hourly_injection_load = np.zeros(8760)
list_of_test_objects.add(SizingObject(borefield, L4_output=244.04826670835274, quadrant=4, name='No injection L4'))

hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\hourly_profile.csv"))
borefield.load = hourly_load
borefield.load.hourly_extraction_load = np.zeros(8760)
list_of_test_objects.add(SizingObject(borefield, L4_output=305.55338863384287, quadrant=2, name='No extraction L4'))

borefield = Borefield(load=MonthlyGeothermalLoadAbsolute(*load_case(2)))
borefield.set_ground_parameters(GroundFluxTemperature(3, 12))
borefield.create_rectangular_borefield(10, 12, 6, 6, 110, 4, 0.075)
borefield.set_Rb(0.2)
list_of_test_objects.add(
    SizingObject(borefield, error_L2=UnsolvableDueToTemperatureGradient, error_L3=UnsolvableDueToTemperatureGradient,
                 quadrant=2, name='Cannot size'))
list_of_test_objects.add(SizingObject(borefield, error_L4=ValueError, quadrant=2, name='Cannot size L4'))

data = GroundConstantTemperature(3, 10)
borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 110, 4, 0.075)
borefield = Borefield()
borefield.set_max_avg_fluid_temperature(16)
borefield.set_min_avg_fluid_temperature(0)
borefield.set_ground_parameters(data)
borefield.set_Rb(0.2)
borefield.set_borefield(borefield_gt)
hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\hourly_profile.csv"))
borefield.load = hourly_load
temp = hourly_load.hourly_extraction_load
temp[0] = 100_000
borefield._borefield_load.hourly_extraction_load = temp
list_of_test_objects.add(
    SizingObject(borefield, L4_output=18760.64149089075, quadrant=4, name='Hourly profile, quadrant 4'))

hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\hourly_profile.csv"), col_injection=0,
                                col_extraction=1)
borefield.load = hourly_load
list_of_test_objects.add(
    SizingObject(borefield, L4_output=368.50138222702657, quadrant=2, name='Hourly profile reversed'))

temp = hourly_load.hourly_extraction_load
temp[0] = 100_000
borefield._borefield_load.hourly_extraction_load = temp
list_of_test_objects.add(
    SizingObject(borefield, L4_output=18602.210559679363, quadrant=3, name='Hourly profile, quadrant 3'))
hourly_load = HourlyBuildingLoad(efficiency_heating=10 ** 6, efficiency_cooling=10 ** 6)
hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\hourly_profile.csv"))
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 87.506, 97.012,
                                                   305.842, 384.204, 230.193, 292.212,
                                                   name='Optimise load profile 1 (power)', power=True, hourly=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 100, 70.054, 87.899,
                                                   210.800, 247.186, 325.236, 429.231,
                                                   name='Optimise load profile 2 (power)', power=True, hourly=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 50, 45.096, 63.799,
                                                   118.898, 117.804, 417.138, 558.612,
                                                   name='Optimise load profile 3 (power)', power=True, hourly=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 87.506, 96.404,
                                                   305.842, 368.463, 230.193, 307.954,
                                                   name='Optimise load profile 1 (power, hourly)', power=True,
                                                   hourly=True))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 100, 69.662, 87.022,
                                                   209.053, 239.590, 326.983, 436.827,
                                                   name='Optimise load profile 2 (power, hourly)', power=True,
                                                   hourly=True))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 50, 44.635, 63.467,
                                                   117.388, 116.699, 418.648, 559.718,
                                                   name='Optimise load profile 3 (power, hourly)', power=True,
                                                   hourly=True))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 93.2297, 99.577,
                                                   536.035, 663.782, 233.4426, 287.344,
                                                   name='Optimise load profile 1 (energy)', power=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 100, 77.543, 96.331,
                                                   385.653, 417.8915, 316.2857, 419.908,
                                                   name='Optimise load profile 2 (energy)', power=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 50, 50.771, 75.461,
                                                   181.332, 209.819, 402.0338, 553.2355,
                                                   name='Optimise load profile 3 (energy)', power=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 67.621, 81.579,
                                                   200, 200, 336.036, 476.416,
                                                   name='Optimise load profile 1 (power, limit)', power=True,
                                                   hourly=False,
                                                   max_peak_heating=200, max_peak_cooling=200))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 67.621, 81.579,
                                                   200, 200, 336.036, 476.416,
                                                   name='Optimise load profile 1 (energy, limit)', power=False,
                                                   max_peak_heating=200, max_peak_cooling=200))

borefield.set_min_avg_fluid_temperature(-5)
borefield.set_max_avg_fluid_temperature(25)
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 100, 100,
                                                   536.036, 676.417, 0, 0, name='Optimise load profile 100% (power)',
                                                   power=True, hourly=False))

list_of_test_objects.add(
    OptimiseLoadProfileObject(borefield, hourly_load, 150, 81.451, 95.049,
                              536.036 / 2, 676.417 / 2, 536.036 / 2, 676.417 / 2,
                              name='Optimise load profile 50% (power)',
                              power=True, hourly=False, max_peak_heating=536.036 / 2,
                              max_peak_cooling=676.417 / 2))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 100, 100,
                                                   536.036, 676.417, 0, 0,
                                                   name='Optimise load profile 100% (power, hourly)', power=True,
                                                   hourly=True))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 100, 100,
                                                   536.036, 676.417, 0, 0, name='Optimise load profile 100% (energy)',
                                                   power=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 81.451, 95.049,
                                                   536.036 / 2, 676.417 / 2, 536.036 / 2, 676.417 / 2,
                                                   name='Optimise load profile 50% (energy)',
                                                   power=False, max_peak_heating=536.036 / 2,
                                                   max_peak_cooling=676.417 / 2))

borefield = Borefield()
borefield.set_ground_parameters(data)
borefield.set_Rb(0.2)
borefield.set_borefield(borefield_gt)
borefield.set_max_avg_fluid_temperature(16)
borefield.set_min_avg_fluid_temperature(0)
hourly_load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\hourly_profile.csv"), col_heating=1,
                                col_cooling=0)
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 99.976, 66.492,
                                                   643.137, 195.331, 33.278, 340.705,
                                                   name='Optimise load profile 1, reversed (power)', power=True,
                                                   hourly=False))
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 99.971, 66.424,
                                                   639.283, 195.053, 37.132, 340.983,
                                                   name='Optimise load profile 1, reversed (power, hourly)', power=True,
                                                   hourly=True))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 99.999, 72.205,
                                                   676.415, 345.9849, 22.46646, 342.1411,
                                                   name='Optimise load profile 1, reversed (energy)', power=False))
borefield.set_max_avg_fluid_temperature(20)
borefield.set_min_avg_fluid_temperature(4)
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 97.012, 87.506,
                                                   384.204, 305.842, 292.211, 230.195,
                                                   name='Optimise load profile 2, reversed (power)', power=True,
                                                   hourly=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 100, 87.899, 70.054,
                                                   247.186, 210.800, 429.23, 325.236,
                                                   name='Optimise load profile 3, reversed (power)', power=True,
                                                   hourly=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 96.404, 87.506,
                                                   368.463, 305.842, 307.953, 230.195,
                                                   name='Optimise load profile 2, reversed (power, hourly)', power=True,
                                                   hourly=True))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 100, 87.022, 69.662,
                                                   239.590, 209.053, 436.826, 326.984,
                                                   name='Optimise load profile 3, reversed (power, hourly)', power=True,
                                                   hourly=True))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 150, 99.577, 93.230,
                                                   663.782, 536.037, 287.343, 233.4438,
                                                   name='Optimise load profile 2, reversed (energy)', power=False))

list_of_test_objects.add(OptimiseLoadProfileObject(borefield, hourly_load, 100, 96.331, 77.543,
                                                   417.8919, 385.6529, 419.9076, 316.2865,
                                                   name='Optimise load profile 3, reversed (energy)', power=False))

borefield = Borefield()
borefield.create_rectangular_borefield(3, 6, 6, 6, 146, 4)
borefield.set_min_avg_fluid_temperature(3)
borefield.set_max_avg_fluid_temperature(16)
borefield.load.peak_duration = 6
load = HourlyBuildingLoad(efficiency_heating=4, efficiency_cooling=25)
load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\problem_data.csv"), col_heating=0,
                         col_cooling=1, header=True, decimal_seperator=',')
load.simulation_period = 40
borefield.load = load

borefield.set_ground_parameters(GroundTemperatureGradient(1.9, 10, gradient=2))
borefield.set_fluid_parameters(FluidData(0.1, 0.475, 1033, 3930, 0.001))
borefield.set_pipe_parameters(SingleUTube(1.5, 0.016, 0.02, 0.42, 0.04))
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, load, 146, 81.5183, 88.0269,
                                                   22.2353, 39.3994, 55.3678, 58.51623,
                                                   name='Optimise load profile (stuck in loop) (power)', power=True,
                                                   hourly=False))
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, load, 146, 80.3414, 84.7223,
                                                   21.65199, 35.8583, 56.14555, 61.92114,
                                                   name='Optimise load profile (stuck in loop) (power, hourly)',
                                                   power=True, hourly=True))
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, load, 146, 89.1681, 97.6848,
                                                   56.49199, 71.1038, 55.13048, 66.55643,
                                                   name='Optimise load profile (stuck in loop) (energy)', power=False))

ground_data = GroundFluxTemperature(3, 10)
fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
pipe_data = DoubleUTube(1, 0.015, 0.02, 0.4, 0.05)
borefield = Borefield()
borefield.create_rectangular_borefield(5, 4, 6, 6, 110, 4, 0.075)
borefield.set_ground_parameters(ground_data)
borefield.set_fluid_parameters(fluid_data)
borefield.set_pipe_parameters(pipe_data)
borefield.calculation_setup(use_constant_Rb=False)
borefield.set_max_avg_fluid_temperature(17)
borefield.set_min_avg_fluid_temperature(3)
hourly_load_building = HourlyBuildingLoad()
hourly_load_building.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\\auditorium.csv"), header=True,
                                         separator=";", col_cooling=0, col_heating=1)
hourly_load_building.hourly_cooling_load = hourly_load_building.hourly_cooling_load * 20 / 21
hourly_load_building.hourly_heating_load = hourly_load_building.hourly_heating_load * 5 / 4
borefield.load = hourly_load_building
list_of_test_objects.add(SizingObject(borefield, L2_output=136.294, L3_output=136.294, L4_output=101.285, quadrant=1,
                                      name='BS2023 Auditorium'))

borefield = Borefield()
borefield.create_rectangular_borefield(10, 10, 6, 6, 110, 4, 0.075)
borefield.set_ground_parameters(ground_data)
borefield.set_fluid_parameters(fluid_data)
borefield.set_pipe_parameters(pipe_data)
borefield.calculation_setup(use_constant_Rb=False)
borefield.set_max_avg_fluid_temperature(17)
borefield.set_min_avg_fluid_temperature(3)
hourly_load_building.simulation_period = 20
hourly_load_building.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\office.csv"), header=True,
                                         separator=";", col_cooling=0, col_heating=1)
hourly_load_building.hourly_cooling_load = hourly_load_building.hourly_cooling_load * 20 / 21
hourly_load_building.hourly_heating_load = hourly_load_building.hourly_heating_load * 5 / 4
borefield.load = hourly_load_building
list_of_test_objects.add(
    SizingObject(borefield, L2_output=113.069, L3_output=113.069, L4_output=107.08131844420905, quadrant=2,
                 name='BS2023 Office'))

borefield = Borefield()
borefield.create_rectangular_borefield(15, 20, 6, 6, 110, 4, 0.075)
borefield.set_ground_parameters(ground_data)
borefield.set_fluid_parameters(fluid_data)
borefield.set_pipe_parameters(pipe_data)
borefield.calculation_setup(use_constant_Rb=False)
borefield.set_max_avg_fluid_temperature(17)
borefield.set_min_avg_fluid_temperature(3)
hourly_load_building.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\swimming_pool.csv"), header=True,
                                         separator=";", col_cooling=0, col_heating=1)
hourly_load_building.hourly_cooling_load = hourly_load_building.hourly_cooling_load * 20 / 21
hourly_load_building.hourly_heating_load = hourly_load_building.hourly_heating_load * 5 / 4
borefield.load = hourly_load_building
list_of_test_objects.add(SizingObject(borefield, L2_output=310.725, L3_output=310.725, L4_output=308.269, quadrant=4,
                                      name='BS2023 Swimming pool'))

eer_combined = EERCombined(20, 5, 10)
borefield = Borefield()
borefield.create_rectangular_borefield(3, 6, 6, 6, 146, 4)
borefield.set_min_avg_fluid_temperature(3)
borefield.set_max_avg_fluid_temperature(16)
borefield.load.peak_duration = 6
load = HourlyBuildingLoad(efficiency_heating=4, efficiency_cooling=eer_combined)
# column order is inverted
load.load_hourly_profile(FOLDER.joinpath("test\methods\hourly_data\hourly_profile.csv"), col_heating=1, col_cooling=0)
load.simulation_period = 40
borefield.load = load

borefield.set_ground_parameters(GroundTemperatureGradient(1.9, 10, gradient=2))
borefield.set_fluid_parameters(FluidData(0.1, 0.475, 1033, 3930, 0.001))
borefield.set_pipe_parameters(SingleUTube(1.5, 0.016, 0.02, 0.42, 0.04))
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, load, 146, 45.978137699335, 11.029080983424729,
                                                   52.82586122830533, 28.00877268650213, 605.9817888622596,
                                                   512.6954920945816,
                                                   name='Optimise load profile (eer combined) (power)', power=True,
                                                   hourly=False))
list_of_test_objects.add(OptimiseLoadProfileObject(borefield, load, 146, 38.165390819460434, 4.08828744800462,
                                                   75.9124206410309, 86.06503815919983, 631.1307699700886, 535.936136,
                                                   name='Optimise load profile (eer combined) (energy)', power=False,
                                                   hourly=False))
