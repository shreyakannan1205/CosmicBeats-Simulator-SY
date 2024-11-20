import subprocess
import os
import re
from datetime import timedelta

#repetitions = int(input("Enter the number of repetitions: "))

repetitions = 40
folder_name = os.getcwd()
num_sat = 1000

distance = [10,20,50]

for d in distance:
    for i in range(0, repetitions):
        input_tle = os.path.join(folder_name, "imaging_num.tle")
        config_file = os.path.join(folder_name + "/configs", f"config_{num_sat}_{d}.json")
        output_file =  os.path.join(folder_name + "/outputs", f"output_{num_sat}_{d}.txt")
        gs_file = os.path.join(folder_name + "/gs_coordinates", f"gs_{d}.txt")

        try:
            command1 = f"python3.11 -m change_tle starlink_original.tle {input_tle} {num_sat}" #Question: we use change_tle.py to extract satellites from starlink. Here it randomly chooses, is this how we want it to be?
            subprocess.run(command1, shell=True, check=True)
            print("done with command 1", d, ":",i)

            command2 = f"python3.11 -m create_config {input_tle} {gs_file} '2024-04-09 12:00:00' '2024-04-09 13:00:00' '15' {config_file}" #what do we set as the delta?
            subprocess.run(command2, shell=True, check=True)
            print("done with command 2", d, ":",i)

            command3 = f"python3.11 -m imagesatellite {config_file} > {output_file}"
            subprocess.run(command3, shell=True, check=True)
            print("done with command 3", d, ":",i)
        
        except Exception as e:
            print("error with command e")
        
    break

