"""
The work of (Ahmadfard and Bernier, 2019) provides a set of test cases that can be used to compare
software tools with the ultimate goal of improving the reliability of design methods for sizing
vertical ground heat exchangers. This document delivers the results on the test file using the GHEtool
L2-, L3- and L4-sizing methods.

Sensitivity analysis on Test 4

References:
-----------
    - Ahmadfard, M., and M. Bernier. 2019. A review of vertical ground heat exchanger sizing tools including an inter-model
comparison [in eng]. Renewable sustainable energy reviews (OXFORD) 110:247–265.
"""
import os
import time

import numpy as np

from GHEtool import *


def test_4_sensitivity():
    # Results from Test 4
    depth_L2s = 121.50772080500283
    depth_L3s = 122.15337731354852
    depth_L4s = 119.99581098989934

    ## Peak magnitude 1 --PM_1
    # -125.7581 kW
    # change peak mangnitude for all (3) months with higher cooling peaks

    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.9, T_g=15, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(5, 5, 8, 8, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # load the monthly profile
    baseload_extraction = np.array([7.938 * 744, 3.784 * 720, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.853 * 744])
    baseload_injection = np.array(
        [0, 0, 8.085 * 744, 21.107 * 720, 35.048 * 744, 43.666 * 720, 46.983 * 744, 44.389 * 744, 34.678 * 720,
         18.686 * 744, 2.983 * 720, 0])
    peak_extraction = np.array([64.946, 60.735, 43.518, 37.849, 0, 0, 0, 0, 0, 5.737, 42.315, 57.209])
    peak_injection = np.array(
        [35.77, 53.548, 83.086, 93.549, 120.782, 125.7581, 125.7581, 125.7581, 111.780, 97.338, 52.843, 34.284])

    load = MonthlyGeothermalLoadAbsolute(baseload_extraction=baseload_extraction, baseload_injection=baseload_injection,
                                         peak_extraction=peak_extraction, peak_injection=peak_injection,
                                         simulation_period=20)
    borefield.load = load

    # convert inlet fluid temperature to heap pump constraints to constraints on average fluid temperature
    delta_t = max(load.max_peak_injection, load.max_peak_extraction) * 1000 / (fluid_data.Cp * fluid_data.mfr) / 25

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_PM_1 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_PM_1 = (depth_L2s_PM_1 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_PM_1 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_PM_1 = (depth_L3s_PM_1 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    ## Peak magnitude 2 --PM_2
    # -153.7044 kW
    # change the peak value this new peak magnitude

    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.9, T_g=15, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(5, 5, 8, 8, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # load the hourly profile
    # 
    baseload_extraction = np.array([7.938 * 744, 3.784 * 720, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.853 * 744])
    baseload_injection = np.array(
        [0, 0, 8.085 * 744, 21.107 * 720, 35.048 * 744, 43.666 * 720, 46.983 * 744, 44.389 * 744, 34.678 * 720,
         18.686 * 744, 2.983 * 720, 0])
    peak_extraction = np.array([64.946, 60.735, 43.518, 37.849, 0, 0, 0, 0, 0, 5.737, 42.315, 57.209])
    peak_injection = np.array(
        [35.77, 53.548, 83.086, 93.549, 120.782, 130.893, 153.7044, 131.761, 111.780, 97.338, 52.843, 34.284])

    load = MonthlyGeothermalLoadAbsolute(baseload_extraction=baseload_extraction, baseload_injection=baseload_injection,
                                         peak_extraction=peak_extraction, peak_injection=peak_injection,
                                         simulation_period=20)
    borefield.load = load

    # convert inlet fluid temperature to heap pump constraints to constraints on average fluid temperature
    delta_t = max(load.max_peak_injection, load.max_peak_extraction) * 1000 / (fluid_data.Cp * fluid_data.mfr) / 25

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_PM_2 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_PM_2 = (depth_L2s_PM_2 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_PM_2 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_PM_2 = (depth_L3s_PM_2 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    ## Thermal Conductivity 1 --TC_1    
    # 1.5 W/m-K
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.5, T_g=15, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(5, 5, 8, 8, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'test4.csv'), header=True, separator=",",
                             col_extraction=1, col_injection=0)
    borefield.load = load

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_TC_1 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_TC_1 = (depth_L2s_TC_1 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_TC_1 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_TC_1 = (depth_L3s_TC_1 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    # according to L4
    L4s_start = time.time()
    depth_L4s_TC_1 = borefield.size(100, L4_sizing=True)
    Var_depth_L4s_TC_1 = (depth_L4s_TC_1 - depth_L4s) / depth_L4s * 100
    L4s_stop = time.time()

    ## Thermal Conductivity 2 --TC_2    
    # 2.3 W/m-K
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=2.3, T_g=15, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(5, 5, 8, 8, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'test4.csv'), header=True, separator=",",
                             col_extraction=1, col_injection=0)
    borefield.load = load

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_TC_2 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_TC_2 = (depth_L2s_TC_2 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_TC_2 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_TC_2 = (depth_L3s_TC_2 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    # according to L4
    L4s_start = time.time()
    depth_L4s_TC_2 = borefield.size(100, L4_sizing=True)
    Var_depth_L4s_TC_2 = (depth_L4s_TC_2 - depth_L4s) / depth_L4s * 100
    L4s_stop = time.time()

    ## Spacing 1 --S_1
    # 6 m 
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.9, T_g=15, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(5, 5, 6, 6, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'test4.csv'), header=True, separator=",",
                             col_extraction=1, col_injection=0)
    borefield.load = load

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_S_1 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_S_1 = (depth_L2s_S_1 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_S_1 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_S_1 = (depth_L3s_S_1 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    # according to L4
    L4s_start = time.time()
    depth_L4s_S_1 = borefield.size(100, L4_sizing=True)
    Var_depth_L4s_S_1 = (depth_L4s_S_1 - depth_L4s) / depth_L4s * 100
    L4s_stop = time.time()

    ## Spacing 2 --S_2
    # 10 m 
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.9, T_g=15, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(5, 5, 10, 10, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'test4.csv'), header=True, separator=",",
                             col_extraction=1, col_injection=0)
    borefield.load = load

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_S_2 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_S_2 = (depth_L2s_S_2 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_S_2 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_S_2 = (depth_L3s_S_2 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    # according to L4
    L4s_start = time.time()
    depth_L4s_S_2 = borefield.size(100, L4_sizing=True)
    Var_depth_L4s_S_2 = (depth_L4s_S_2 - depth_L4s) / depth_L4s * 100
    L4s_stop = time.time()

    ## Ground temperature 1 --GT_1
    # 10 C 
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.9, T_g=10, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(5, 5, 8, 8, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'test4.csv'), header=True, separator=",",
                             col_extraction=1, col_injection=0)
    borefield.load = load

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_GT_1 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_GT_1 = (depth_L2s_GT_1 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_GT_1 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_GT_1 = (depth_L3s_GT_1 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    # according to L4
    L4s_start = time.time()
    depth_L4s_GT_1 = borefield.size(100, L4_sizing=True)
    Var_depth_L4s_GT_1 = (depth_L4s_GT_1 - depth_L4s) / depth_L4s * 100
    L4s_stop = time.time()

    ## Ground temperature 2 --GT_2
    # 20 C 
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.9, T_g=20, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(5, 5, 8, 8, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'test4.csv'), header=True, separator=",",
                             col_extraction=1, col_injection=0)
    borefield.load = load

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_GT_2 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_GT_2 = (depth_L2s_GT_2 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_GT_2 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_GT_2 = (depth_L3s_GT_2 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    # according to L4
    L4s_start = time.time()
    depth_L4s_GT_2 = borefield.size(100, L4_sizing=True)
    Var_depth_L4s_GT_2 = (depth_L4s_GT_2 - depth_L4s) / depth_L4s * 100
    L4s_stop = time.time()

    ## Boreholes numbers 1 --BN_1
    # 3x3 bores
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.9, T_g=15, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(3, 3, 8, 8, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'test4.csv'), header=True, separator=",",
                             col_extraction=1, col_injection=0)
    borefield.load = load

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_BN_1 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_BN_1 = (depth_L2s_BN_1 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_BN_1 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_BN_1 = (depth_L3s_BN_1 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    # according to L4
    L4s_start = time.time()
    depth_L4s_BN_1 = borefield.size(100, L4_sizing=True)
    Var_depth_L4s_BN_1 = (depth_L4s_BN_1 - depth_L4s) / depth_L4s * 100
    L4s_stop = time.time()

    ## Boreholes numbers 2 --BN_2
    # 7x7 bores
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=1.9, T_g=15, volumetric_heat_capacity=2052000, flux=0)
    fluid_data = FluidData(mfr=0.074 * 139.731 / 25, rho=1026, Cp=4019, mu=0.003377, k_f=0.468)
    pipe_data = MultipleUTube(r_in=0.013, r_out=0.0167, D_s=0.083 / 2, k_g=0.69, k_p=0.4)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(7, 7, 8, 8, 110, 4, 0.075)
    Rb_static = 0.2
    borefield.set_Rb(Rb_static)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(38 + delta_t / 2)
    borefield.set_min_avg_fluid_temperature(0 - delta_t / 2)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'test4.csv'), header=True, separator=",",
                             col_extraction=1, col_injection=0)
    borefield.load = load

    # Sizing with constant Rb
    L2s_start = time.time()
    depth_L2s_BN_2 = borefield.size(100, L2_sizing=True)
    Var_depth_L2s_BN_2 = (depth_L2s_BN_2 - depth_L2s) / depth_L2s * 100
    L2s_stop = time.time()

    # according to L3
    L3s_start = time.time()
    depth_L3s_BN_2 = borefield.size(100, L3_sizing=True)
    Var_depth_L3s_BN_2 = (depth_L3s_BN_2 - depth_L3s) / depth_L3s * 100
    L3s_stop = time.time()

    # according to L4
    L4s_start = time.time()
    depth_L4s_BN_2 = borefield.size(100, L4_sizing=True)
    Var_depth_L4s_BN_2 = (depth_L4s_BN_2 - depth_L4s) / depth_L4s * 100
    L4s_stop = time.time()

    print(
        f"The sizing according to L2 has a variation of length of {Var_depth_L2s_PM_1:.2f}% and {Var_depth_L2s_PM_2:.2f}% (Peak Magn. -125.7581 and -153.7044 kW), {Var_depth_L2s_TC_1:.2f}% and {Var_depth_L2s_TC_2:.2f}% (Therm. cond. 1.5 and 2.3 W/m-K), {Var_depth_L2s_S_1:.2f}% en {Var_depth_L2s_S_2:.2f}% (6 and 10 m spacing), {Var_depth_L2s_GT_1:.2f}% en {Var_depth_L2s_GT_2:.2f}% (Ground Temp. 10 and 20 C), {Var_depth_L2s_BN_1:.2f}% en {Var_depth_L2s_BN_2:.2f}% (3x3 and 7x7 bores). ")
    print(
        f"The sizing according to L3 has a variation of length of {Var_depth_L3s_PM_1:.2f}% and {Var_depth_L3s_PM_2:.2f}% (Peak Magn. -125.7581 and -153.7044 kW), {Var_depth_L3s_TC_1:.2f}% and {Var_depth_L3s_TC_2:.2f}% (Therm. cond. 1.5 and 2.3 W/m-K), {Var_depth_L3s_S_1:.2f}% en {Var_depth_L3s_S_2:.2f}% (6 and 10 m spacing), {Var_depth_L3s_GT_1:.2f}% en {Var_depth_L3s_GT_2:.2f}% (Ground Temp. 10 and 20 C), {Var_depth_L3s_BN_1:.2f}% en {Var_depth_L3s_BN_2:.2f}% (3x3 and 7x7 bores). ")
    print(
        f"The sizing according to L4 has a variation of length of ---- and ---- (Peak Magn. -125.7581 and -153.7044 kW), {Var_depth_L4s_TC_1:.2f}% and {Var_depth_L4s_TC_2:.2f}% (Therm. cond. 1.5 and 2.3 W/m-K), {Var_depth_L4s_S_1:.2f}% en {Var_depth_L4s_S_2:.2f}% (6 and 10 m spacing), {Var_depth_L4s_GT_1:.2f}% en {Var_depth_L4s_GT_2:.2f}% (Ground Temp. 10 and 20 C), {Var_depth_L4s_BN_1:.2f}% en {Var_depth_L4s_BN_2:.2f}% (3x3 and 7x7 bores). ")


if __name__ == "__main__":  # pragma: no cover
    test_4_sensitivity()
