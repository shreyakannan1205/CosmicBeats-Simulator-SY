import subprocess
import os

# Create the NumSat directory if it does not exist
folder_name = "NumSat"
os.makedirs(folder_name, exist_ok=True)

# List of numbers to replace in the commands
numbers = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 3000]  # 5707

for num in numbers:
    # File paths are now prefixed with the folder name
    input_tle = os.path.join(folder_name, "imaging_num.tle")
    output_json = os.path.join(folder_name, f"output_file_{num}_random.json")
    output_txt = os.path.join(folder_name, f"output_{num}_random.txt")

    command1 = f"python3 change_tle.py starlink_original.tle {input_tle} {num}"
    command2 = f"python3 create_config.py {input_tle} gs.txt '2024-04-09 12:00:00' '2024-04-10 12:00:00' '1' {output_json}"
    command3 = f"python3 imagesatellite.py {output_json} > {output_txt}"
    command4 = f"python3 output_examine.py {output_txt}"

    try:
        print(f"Running commands for number: {num}")
        subprocess.run(command1, shell=True, check=True)
        subprocess.run(command2, shell=True, check=True)
        subprocess.run(command3, shell=True, check=True)
        subprocess.run(command4, shell=True, check=True)
        print(f"Completed commands for number: {num}\n")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
