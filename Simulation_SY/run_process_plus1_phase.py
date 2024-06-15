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

def process_source_file(source_file, base_name, gs_file):
    num_satellites = count_satellites(source_file)
    directory = "PlusOne_Phase"
    os.makedirs(directory, exist_ok=True)

    run_script(f"python3 create_config.py {directory}/original_4.tle gs/{gs_file} '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_initial_plus1_{base_name}.json")
    run_script(f"python3 imagesatellite.py {directory}/output_initial_plus1_{base_name}.json > {directory}/output_initial_plus1_{base_name}.txt")
    run_script(f"python3 output_examine.py {directory}/output_initial_plus1_{base_name}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
    run_script(f"python3 gap_duration_analysis.py {directory}/output_initial_plus1_{base_name}_gaps_report.txt {directory}/gap_duration_analysis_initial_plus1_{base_name}.txt")

    for i in range(num_satellites):
        print(f"Cycle {i + 1} for satellite {i} starts with {base_name}.")
        run_script(f"python3 change_tle_plus1_ablation.py {source_file} {directory}/original_4.tle {directory}/gap_duration_analysis_plus1_{base_name}.txt {i}")
        run_script(f"python3 create_config.py {directory}/original_4.tle gs/{gs_file} '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_plus1_{base_name}.json")
        run_script(f"python3 imagesatellite.py {directory}/output_plus1_{base_name}.json > {directory}/output_plus1_{base_name}.txt")
        run_script(f"python3 output_examine.py {directory}/output_plus1_{base_name}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
        run_script(f"python3 gap_duration_analysis.py {directory}/output_plus1_{base_name}_gaps_report.txt {directory}/gap_duration_analysis_plus1_{base_name}.txt")
        run_script(f"python3 change_tle_to_original.py {directory}/original_4.tle")

        print(f"Satellite {i + 1} completed at {base_name}.")

def main():
    source_file = "PlusOne_Phase/imaginary.tle"
    ground_stations = [
        ("gs_tw.txt", "taipei"),
        ("gs_ny.txt", "ny"),
        ("gs_sp.txt", "saopaulo"),
        ("gs_mum.txt", "mumbai"),
        ("gs_la.txt", "la"),
        ("gs_lg.txt", "lagos"),
        ("gs_mos.txt", "moscow"),
        ("gs_sy.txt", "sydney"),
        ("gs_sk.txt", "seoul"),
        ("gs_pa.txt", "paris")
    ]

    for gs_file, base_name in ground_stations:
        process_source_file(source_file, base_name, gs_file)

if __name__ == "__main__":
    main()
