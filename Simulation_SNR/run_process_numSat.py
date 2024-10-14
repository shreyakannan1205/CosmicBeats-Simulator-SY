import subprocess
import os
import re
from datetime import timedelta

repetitions = int(input("Enter the number of repetitions: "))

folder_name = "NumSat_Taipei"
folder_name1 = "/home/seoyul/"
os.makedirs(folder_name, exist_ok=True)

# numbers = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 3000]
numbers = [5000]

for num in numbers:
    target_gap_duration_file = os.path.join(folder_name, f"total_gap_duration_analysis_{num}.txt")

    open(target_gap_duration_file, 'w').close()

    for rep in range(1, repetitions + 1):
        input_tle = os.path.join(folder_name, "imaging_num.tle")
        output_json = os.path.join(folder_name, f"output_file_{num}_random.json")
        output_txt = os.path.join(folder_name1, f"output_{num}_random.txt")
       
        command1 = f"python3 change_tle.py starlink_original.tle {input_tle} {num}"
        command2 = f"python3 create_config_v2.py {input_tle} gs_tp.txt '2024-04-09 12:00:00' '2024-04-09 13:00:00' '1' {output_json}"
        command3 = f"python3 imagesatellite.py {output_json} > {output_txt}"


        try:
            print(f"Running commands for number: {num}, repetition: {rep}")
            subprocess.run(command1, shell=True, check=True)
            subprocess.run(command2, shell=True, check=True)
            subprocess.run(command3, shell=True, check=True)
 
            print(f"Completed commands for number: {num}, repetition: {rep}\n")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

print("Script completed.")
