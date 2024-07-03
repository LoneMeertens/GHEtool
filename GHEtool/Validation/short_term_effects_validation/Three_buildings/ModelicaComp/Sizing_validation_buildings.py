import pandas as pd
from pathlib import Path
import numpy as np
import os
import time
import argparse

### READ ARGUMMENTS ###
# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='This script is used to simulate a given borefield using Modelica')

# Add command-line arguments
parser.add_argument('-mos', '--mos_name', help='Specify mos-file name') # Specify the name of the mos-file
parser.add_argument('-length', help='Specify borehole length') # Specify borehole length
parser.add_argument('-Tmin', help='Specify minimum inlet fluid temperature to the heat pump') # Specify T_{L}
parser.add_argument('-Tmax', help='Specify maximum inlet fluid temperature to the heat pump') # Specify T_{H}
parser.add_argument('-Tg', help='Specify undisturbed ground temperature') # Specify T_g
parser.add_argument('-lifetime', help='Specify the amount of years to consider in the borefield sizing', default=10) # Specify the lifetime of the borefield
parser.add_argument('-use_Rb', help='Specify if Rb is calculated (false) or imposed (true)' ) # Specify true/false setting of parameter use_Rb

# Parse the arguments
args = parser.parse_args()

# Access the value of the argument
mos_name = args.mos_name
mos_name_without_mos = Path(mos_name).stem
length = float(args.length)
Tf_min =float(args.Tmin)
Tf_max = float(args.Tmax)
Tg = float(args.Tg)
lifetime = int(args.lifetime)
use_Rb = args.use_Rb

print(f"parameters: mos_name = {mos_name}, length = {length}, Tf_min = {Tf_min}, Tf_max = {Tf_max}, Tg = {Tg}, lifetime = {lifetime}, use_Rb = {use_Rb}")


Mos_path = f"/home/u0169319//Workdir/boropt/lone/ValidationTests/Buildings/{mos_name}" # Absolute path to the mos file for the borefield simulation

### CREATE THE FOLDER TO STORE THE RESULTS ###
# Define the folder path
folder_name = f"{mos_name_without_mos}"
sub_folder_name = f"{mos_name_without_mos}"
mainfolder_path = f"/home/u0169319/Documents/Develop/boropt/Sizing/Buildings/{folder_name}"
results_path = f"{mainfolder_path}/Results" # Absolute path of a folder in the mainfolder_path to store the sizing results

# if the folder already exists, remove it and create a new onemop
if os.path.exists(mainfolder_path):
    os.system(f"rm -r {mainfolder_path}")
os.system(f"mkdir {mainfolder_path}") # Create a folder for the specific approach

def size_borefield_Mod(hBor_init, Tmin, Tmax, T_cte): ### !!!! A better algorithm should be implemented to size the borefield with Modelica !!!
    # This function sizes the borefield with Modelica and returns the length of the borefield toghether with the temperature profile
    hBor = hBor_init
    dif = 1000
    depths = np.array([])
    n_iteration = 0
    while dif > 0.05:
        n_iteration = n_iteration + 1
        print(f"Iteration number {n_iteration}")
        mult_fac = np.array([]) #multiplaction factor on Lprev to get new L
        print(f"T Difference is {dif} \n")
        print(f"Current depth of borefield: {hBor} \n")
        depths = np.append(depths, hBor)
        print("Simulation of TEva using modelica \n")
        Tmean = simulate_borefield(hBor=hBor)
        Tminimal = Tmean.min()
        Tmaximal = Tmean.max()
        print(f"Minimal temperature of the borefield with lenght of {hBor}m: {Tminimal} \n")
        print(f"Maximal temperature of the borefield with lenght of {hBor}m: {Tmaximal} \n")
        criteria1 = (Tmaximal - T_cte)/(Tmax - T_cte)  
        criteria2 = (Tminimal - T_cte)/(Tmin - T_cte)
        mult_fac = np.append(criteria1, criteria2) #Same iterative loop as implemented in GHEtool 
        hBorPrev = hBor
        hBor = mult_fac.max()*hBorPrev
        dif = abs(hBorPrev - hBor)
        print(f"Decrease depth of borefield with {dif} \n")
        print("hBor: ", hBor, "\n")

    hBorOpt = hBor
    print(f"Optimal depth of borefield: {hBorOpt} \n")
    Tmean = simulate_borefield(hBorOpt)
    #copy results to results file

    print(f"NUMBER OF ITERATIONS: {n_iteration}")
    return hBorOpt, Tmean

def simulate_borefield(hBor):
    # This function runs the simulation of the borefield model

    ## Change the lines in the base mos file to use the correct load profila and results path
    words = ['cd("FILL_IN_MAINFOLDER_PATH_HERE")', 'borefield.borFieDat.conDat.hBor=', 'borefield.borFieDat.conDat.use_Rb=', 'stopTime']
    new_lines = [f'cd("{mainfolder_path}")', f'\t\t\t\tborefield.borFieDat.conDat.hBor={hBor},', f'\t\t\t\tborefield.borFieDat.conDat.use_Rb={use_Rb})",', f'\t\t\t\tstopTime={lifetime}*365*24*3600,']
															
    # Open the file in read mode
    with open(Mos_path, "r") as mos_file:
        lines = mos_file.readlines()
        # Find the line starting with the initial word
    for i, line in enumerate(lines):
        for word, new_line in zip(words, new_lines):
            if word in line:
                lines[i] = new_line + "\n"
    # Write the modified lines back to the file
    with open(f'{mainfolder_path}/{mos_name}', "w") as file:
        file.writelines(lines)

    path_sim = f"cd {mainfolder_path} ; xvfb-run -a /usr/local/bin/dymola-2024x-x86_64 /nowindow {mainfolder_path}/{mos_name}"
    print(path_sim)

    ## Run the simulation
    print("\n starting DYMOLA for borefield simulation \n")
    os.system(f"cd {mainfolder_path} ; xvfb-run -a /usr/local/bin/dymola-2024x-x86_64 /nowindow {mainfolder_path}/{mos_name}")
    print("DYMOLA FINISHED \n")
    # Read simulation results
    df = pd.read_csv(f"{mainfolder_path}/{folder_name}.csv", sep=';', header=0)
    Tmean = df["TAvgFluid"].values[:-1] #remove last value
    Tmean = Tmean - 273.15 #Convert to °C
    
    return Tmean

print("Sizing of borefield length using modelica \n")

start_sizing = time.time()
L, Tmean = size_borefield_Mod(hBor_init=length, Tmin=Tf_min, Tmax=Tf_max, T_cte=Tg)
stop_sizing = time.time()

Tmean_min = min(Tmean) 
Tmean_max = max(Tmean) 
   
print(f"THE MINIUM OBTAINED FLUID TEMPERATURE: {Tmean_min} °C ")
print(f"THE MAXIMUM OBTAINED FLUID TEMPERATURE: {Tmean_max} °C ")
print(f"THE REQUIRED BOREFIELD LENGHT IS: {L} m")
print(f"THE TIME NEEDED FOR SIZING: {stop_sizing-start_sizing} s")