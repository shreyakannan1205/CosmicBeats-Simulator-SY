import subprocess
import os

def run_script(command):
    """ Helper function to run a shell command. """
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def count_satellites(source_file):
    with open(source_file, 'r') as file:
        lines = file.readlines()
    return len(lines) // 3

def process_source_file(source_file):
    num_satellites = count_satellites(source_file)
    directory = "PlusOne_Phase_24"
    os.makedirs(directory, exist_ok=True)

    # Run initial gap duration analysis
    run_script(f"python3 create_config_v2.py original_24.tle gs.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_plus1_phase.json")
    run_script(f"python3 imagesatellite.py {directory}/output_plus1_phase.json > {directory}/output_plus1_phase.txt")
    run_script(f"python3 correct_lines_in_txt.py {directory}/output_plus1_phase.txt")
    run_script(f"python3 output_examine_v2.py {directory}/output_plus1_phase.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")

    for i in range(num_satellites):
        print(f"Cycle {i + 1} for satellite {i+1} starts.")
        run_script(f"python3 change_tle_plus1_ablation.py {source_file} original_24.tle {i}")
        run_script(f"python3 create_config_v2.py original_24.tle gs.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_plus1_phase.json")
        run_script(f"python3 imagesatellite.py {directory}/output_plus1_phase.json > {directory}/output_plus1_phase.txt")
        run_script(f"python3 correct_lines_in_txt.py {directory}/output_plus1_phase.txt")
        run_script(f"python3 output_examine_v2.py {directory}/output_plus1_phase.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
        run_script(f"python3 change_tle_to_original.py original_24.tle")

        print(f"Satellite {i + 1} completed.")

def main():
    source_file = "imaginary_24.tle"

    process_source_file(source_file)

if __name__ == "__main__":
    main()
