"""
The different L4-model inclusing the short-term effects is validated based on three different buildings: an auditorium, an office and a swimming
pool. The three buildings were simulated previously in IESVE and the resulting heating and cooling demand profiles
were exported (Peere et al., 2023). 

References:
-----------
    - Meertens, L., Peere, W., and Helsen, L. (2024). Influence of short-term dynamic effects on geothermal borefield size. 
In _Proceedings of International Ground Source Heat Pump Association Conference 2024_. Montreal (Canada), 28-30 May 2024. 
https://doi.org/10.22488/okstate.24.000004 
    - Peere, W., L. Hermans, W. Boydens, and L. Helsen. 2023. Evaluation of the oversizing and computational speed of different
open-source borefield sizing methods. BS2023 Conference, Shanghai, China, April
"""
import os
import time

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import sys
sys.path.append("C:\Workdir\Develop\ghetool")

from GHEtool import *

def Swimming_pool():
    #To do:
    #Sensitivity: rhoCp grout and pipe

    ### Case 1 - Constant ground temperature

    ## GHEtool L4
    
    # Rb calculated by tool
    # initiate ground, fluid and pipe data
    ground_data = GroundConstantTemperature(k_s=3, T_g=10, volumetric_heat_capacity= 2.4 * 10**6)
    fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    pipe_data = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05, 1)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(15, 20, 6, 6, 100, 4, 0.075)
    #borefield.set_Rb(0.12)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(17)
    borefield.set_min_avg_fluid_temperature(3)

    # load the hourly profile
    load = HourlyGeothermalLoad(simulation_period=20)
    load.load_hourly_profile(os.path.join(os.path.dirname(__file__), 'swimming_pool.csv'), header=True, separator=";",
                             decimal_seperator=".", col_heating=1,
                             col_cooling=0)
    borefield.load = load

    SEER = 20
    SCOP = 4

    # load hourly heating and cooling load and convert it to geothermal loads
    primary_geothermal_load = HourlyGeothermalLoad(simulation_period=load.simulation_period)
    primary_geothermal_load.set_hourly_cooling(load.hourly_cooling_load.copy() * (1 + 1 / SEER))
    primary_geothermal_load.set_hourly_heating(load.hourly_heating_load.copy() * (1 - 1 / SCOP))
    # set geothermal load
    borefield.load = primary_geothermal_load

    options = {'nSegments': 12,
                'segment_ratios': None,
                   'disp': False,
                   'profiles': True,
                   'method': 'equivalent'
                     }

    borefield.set_options_gfunction_calculation(options)

    # according to L4
    L4_cst_start = time.time()
    depth_L4_cst = borefield.size(100, L4_sizing=True)
    Rb_L4_cst = borefield.Rb
    L4_cst_stop = time.time()
    Tg_L4_cst = borefield._Tg(depth_L4_cst)

    # initiate borefield
    borefield = Borefield()

    ## GHEtool L4 - including short-term effects

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(15, 20, 6, 6, 100, 4, 0.075)
    #borefield.set_Rb(0.12)
    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(17)
    borefield.set_min_avg_fluid_temperature(3)

    # load the hourly profile
    borefield.load = primary_geothermal_load
    # Addidional input data needed for short-term model
    rho_cp_grout = 3900000.0  
    rho_cp_pipe = 1540000.0  

    # Sample dictionary with short-term effect parameters
    short_term_effects_parameters = {
    'rho_cp_grout': rho_cp_grout,
    'rho_cp_pipe': rho_cp_pipe,
    }

    options = {'nSegments': 12,
                   'segment_ratios': None,
                   'disp': False,
                   'profiles': True,
                   'method': 'equivalent',
                   'cylindrical_correction': True,
                   'short_term_effects': True,
                   'ground_data': ground_data,
                   'fluid_data': fluid_data,
                   'pipe_data': pipe_data,
                   'borefield': borefield,
                   'short_term_effects_parameters': short_term_effects_parameters,
                     }

    borefield.set_options_gfunction_calculation(options)

    # according to L4 including short-term effects
    L4_ste_cst_start = time.time()
    depth_L4_ste_cst = borefield.size(100, L4_sizing=True)
    Rb_L4_ste_cst = borefield.Rb
    L4_ste_cst_stop = time.time()
    Tg_L4_ste_cst = borefield._Tg(depth_L4_ste_cst)

    
    ### Case 2 - Temperature gradient in ground = 1 K/100m

    ground_data = GroundTemperatureGradient(k_s=3, T_g=10, volumetric_heat_capacity= 2.4 * 10**6, gradient=1)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(15, 20, 6, 6, 100, 4, 0.075)
    #borefield.set_Rb(0.12)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(17)
    borefield.set_min_avg_fluid_temperature(3)

    # set geothermal load
    borefield.load = primary_geothermal_load

    options = {'nSegments': 12,
                'segment_ratios': None,
                   'disp': False,
                   'profiles': True,
                   'method': 'equivalent'
                     }

    borefield.set_options_gfunction_calculation(options)

    # according to L4
    L4_gradient_1_start = time.time()
    depth_L4_gradient_1 = borefield.size(100, L4_sizing=True)
    Rb_L4_gradient_1 = borefield.Rb
    L4_gradient_1_stop = time.time()
    Tg_L4_gradient_1 = borefield._Tg(depth_L4_gradient_1)

    # initiate borefield
    borefield = Borefield()

    ## GHEtool L4 - including short-term effects

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(15, 20, 6, 6, 100, 4, 0.075)
    #borefield.set_Rb(0.12)
    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(17)
    borefield.set_min_avg_fluid_temperature(3)

    # load the hourly profile
    borefield.load = primary_geothermal_load
    # Addidional input data needed for short-term model
    rho_cp_grout = 3900000.0  
    rho_cp_pipe = 1540000.0  

    # Sample dictionary with short-term effect parameters
    short_term_effects_parameters = {
    'rho_cp_grout': rho_cp_grout,
    'rho_cp_pipe': rho_cp_pipe,
    }

    options = {'nSegments': 12,
                   'segment_ratios': None,
                   'disp': False,
                   'profiles': True,
                   'method': 'equivalent',
                   'cylindrical_correction': True,
                   'short_term_effects': True,
                   'ground_data': ground_data,
                   'fluid_data': fluid_data,
                   'pipe_data': pipe_data,
                   'borefield': borefield,
                   'short_term_effects_parameters': short_term_effects_parameters,
                     }

    borefield.set_options_gfunction_calculation(options)

    # according to L4 including short-term effects
    L4_ste_gradient_1_start = time.time()
    depth_L4_ste_gradient_1 = borefield.size(100, L4_sizing=True)
    Rb_L4_ste_gradient_1 = borefield.Rb
    L4_ste_gradient_1_stop = time.time()
    Tg_L4_ste_gradient_1 = borefield._Tg(depth_L4_ste_gradient_1)

    ### Case 3 - Temperature gradient in ground = 3 K/100m

    ground_data = GroundTemperatureGradient(k_s=3, T_g=10, volumetric_heat_capacity= 2.4 * 10**6, gradient=2)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(15, 20, 6, 6, 100, 4, 0.075)
    #borefield.set_Rb(0.12)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(17)
    borefield.set_min_avg_fluid_temperature(3)

    # set geothermal load
    borefield.load = primary_geothermal_load

    options = {'nSegments': 12,
                'segment_ratios': None,
                   'disp': False,
                   'profiles': True,
                   'method': 'equivalent'
                     }

    borefield.set_options_gfunction_calculation(options)

    # according to L4
    L4_gradient_3_start = time.time()
    depth_L4_gradient_3 = borefield.size(100, L4_sizing=True)
    Rb_L4_gradient_3 = borefield.Rb
    L4_gradient_3_stop = time.time()
    Tg_L4_gradient_3 = borefield._Tg(depth_L4_gradient_3)

    # initiate borefield
    borefield = Borefield()

    ## GHEtool L4 - including short-term effects

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(15, 20, 6, 6, 100, 4, 0.075)
    #borefield.set_Rb(0.12)
    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(17)
    borefield.set_min_avg_fluid_temperature(3)

    # load the hourly profile
    borefield.load = primary_geothermal_load
    # Addidional input data needed for short-term model
    rho_cp_grout = 3900000.0  
    rho_cp_pipe = 1540000.0  

    # Sample dictionary with short-term effect parameters
    short_term_effects_parameters = {
    'rho_cp_grout': rho_cp_grout,
    'rho_cp_pipe': rho_cp_pipe,
    }

    options = {'nSegments': 12,
                   'segment_ratios': None,
                   'disp': False,
                   'profiles': True,
                   'method': 'equivalent',
                   'cylindrical_correction': True,
                   'short_term_effects': True,
                   'ground_data': ground_data,
                   'fluid_data': fluid_data,
                   'pipe_data': pipe_data,
                   'borefield': borefield,
                   'short_term_effects_parameters': short_term_effects_parameters,
                     }

    borefield.set_options_gfunction_calculation(options)

    # according to L4 including short-term effects
    L4_ste_gradient_3_start = time.time()
    depth_L4_ste_gradient_3 = borefield.size(100, L4_sizing=True)
    Rb_L4_ste_gradient_3 = borefield.Rb
    L4_ste_gradient_3_stop = time.time()
    Tg_L4_ste_gradient_3 = borefield._Tg(depth_L4_ste_gradient_3)

    
    ### Case 4 - Temperature flux in ground

    ## GHEtool L4
    
    # Rb calculated by tool
    # initiate ground, fluid and pipe data
    ground_data = GroundFluxTemperature(k_s=3, T_g=10, volumetric_heat_capacity= 2.4 * 10**6, flux=0.06)
    fluid_data = FluidData(0.2, 0.568, 998, 4180, 1e-3)
    pipe_data = MultipleUTube(1, 0.015, 0.02, 0.4, 0.05, 1)

    # initiate borefield
    borefield = Borefield()

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(15, 20, 6, 6, 100, 4, 0.075)
    #borefield.set_Rb(0.12)

    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(17)
    borefield.set_min_avg_fluid_temperature(3)

    # set geothermal load
    borefield.load = primary_geothermal_load

    options = {'nSegments': 12,
                'segment_ratios': None,
                   'disp': False,
                   'profiles': True,
                   'method': 'equivalent'
                     }

    borefield.set_options_gfunction_calculation(options)

    # according to L4
    L4_flux_start = time.time()
    depth_L4_flux = borefield.size(100, L4_sizing=True)
    Rb_L4_flux = borefield.Rb
    L4_flux_stop = time.time()
    Tg_L4_flux = borefield._Tg(depth_L4_flux)

    # initiate borefield
    borefield = Borefield()

    ## GHEtool L4 - including short-term effects

    # set ground data in borefield
    borefield.set_ground_parameters(ground_data)
    borefield.set_fluid_parameters(fluid_data)
    borefield.set_pipe_parameters(pipe_data)
    borefield.create_rectangular_borefield(15, 20, 6, 6, 100, 4, 0.075)
    #borefield.set_Rb(0.12)
    # set temperature bounds
    borefield.set_max_avg_fluid_temperature(17)
    borefield.set_min_avg_fluid_temperature(3)

    # load the hourly profile
    borefield.load = primary_geothermal_load
    # Addidional input data needed for short-term model
    rho_cp_grout = 3900000.0  
    rho_cp_pipe = 1540000.0  

    # Sample dictionary with short-term effect parameters
    short_term_effects_parameters = {
    'rho_cp_grout': rho_cp_grout,
    'rho_cp_pipe': rho_cp_pipe,
    }

    options = {'nSegments': 12,
                   'segment_ratios': None,
                   'disp': False,
                   'profiles': True,
                   'method': 'equivalent',
                   'cylindrical_correction': True,
                   'short_term_effects': True,
                   'ground_data': ground_data,
                   'fluid_data': fluid_data,
                   'pipe_data': pipe_data,
                   'borefield': borefield,
                   'short_term_effects_parameters': short_term_effects_parameters,
                     }

    borefield.set_options_gfunction_calculation(options)

    # according to L4 including short-term effects
    L4_ste_flux_start = time.time()
    depth_L4_ste_flux = borefield.size(100, L4_sizing=True)
    Rb_L4_ste_flux = borefield.Rb
    L4_ste_flux_stop = time.time()
    Tg_L4_ste_flux = borefield._Tg(depth_L4_ste_flux)

    plt.show()


    print('Case 1 - Constant ground temperature')
    print(
        f"The sizing according to L4 has a depth of {depth_L4_cst:.2f}m (using dynamic Rb* of {Rb_L4_cst:.3f}), Tg equals {Tg_L4_cst} °C and time needed for sizing was {L4_cst_stop-L4_cst_start:.2f}s")
    print(
        f"The sizing according to L4 (including ste) has a depth of {depth_L4_ste_cst:.2f}m (using dynamic Rb* of {Rb_L4_ste_cst:.3f}), Tg equals {Tg_L4_ste_cst} °C and time needed for sizing was {L4_ste_cst_stop-L4_ste_cst_start:.2f}s")
    

    print('Case 2 - Temperature gradient in ground = 1 K/100m')
    print(
        f"The sizing according to L4 has a depth of {depth_L4_gradient_1:.2f}m (using dynamic Rb* of {Rb_L4_gradient_1:.3f}), Tg equals {Tg_L4_gradient_1} °C and time needed for sizing was {L4_gradient_1_stop-L4_gradient_1_start:.2f}s")
    print(
        f"The sizing according to L4 (including ste) has a depth of {depth_L4_ste_gradient_1:.2f}m (using dynamic Rb* of {Rb_L4_ste_gradient_1:.3f}), Tg equals {Tg_L4_ste_gradient_1} °C and time needed for sizing was {L4_ste_gradient_1_stop-L4_ste_gradient_1_start:.2f}s")
    
    
    print('Case 3 - Temperature gradient in ground = 3K/100m')
    print(
        f"The sizing according to L4 has a depth of {depth_L4_gradient_3:.2f}m (using dynamic Rb* of {Rb_L4_gradient_3:.3f}), Tg equals {Tg_L4_gradient_3} °C and time needed for sizing was {L4_gradient_3_stop-L4_gradient_3_start:.2f}s")
    print(
        f"The sizing according to L4 (including ste) has a depth of {depth_L4_ste_gradient_3:.2f}m (using dynamic Rb* of {Rb_L4_ste_gradient_3:.3f}), Tg equals {Tg_L4_ste_gradient_3} °C and time needed for sizing was {L4_ste_gradient_3_stop-L4_ste_gradient_3_start:.2f}s")
    
    
    print('Case 4 - Temperature flux in ground')
    print(
        f"The sizing according to L4 has a depth of {depth_L4_flux:.2f}m (using dynamic Rb* of {Rb_L4_flux:.3f}), Tg equals {Tg_L4_flux} °C and time needed for sizing was {L4_flux_stop-L4_flux_start:.2f}s")
    print(
        f"The sizing according to L4 (including ste) has a depth of {depth_L4_ste_flux:.2f}m (using dynamic Rb* of {Rb_L4_ste_flux:.3f}), Tg equals {Tg_L4_ste_flux} °C and time needed for sizing was {L4_ste_flux_stop-L4_ste_flux_start:.2f}s")
    

if __name__ == "__main__":  # pragma: no cover
    Swimming_pool()