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

def process_source_file(source_file, base_name):
    num_satellites = count_satellites(source_file)
    directory = "Ablation"
    os.makedirs(directory, exist_ok=True)

    for i in range(num_satellites):
        print(f"Cycle {i + 1} for satellite {i} starts with {base_name}.")
        run_script(f"python3 change_tle_plus1_ablation.py {source_file} {directory}/starlink_ablation_selected4.tle {directory}/gap_duration_analysis_plus1_{base_name}.txt {i}")
        run_script(f"python3 create_config.py {directory}/starlink_ablation_selected4.tle gs.txt '2024-04-09 12:00:00' '2024-04-10 12:00:00' '1' {directory}/output_plus1_{base_name}.json")
        run_script(f"python3 imagesatellite.py {directory}/output_plus1_{base_name}.json > {directory}/output_plus1_{base_name}.txt")
        run_script(f"python3 output_examine.py {directory}/output_plus1_{base_name}.txt")
        run_script(f"python3 gap_duration_analysis.py {directory}/output_plus1_{base_name}_gaps_report.txt {directory}/gap_duration_analysis_plus1_{base_name}.txt")
        run_script(f"python3 change_tle_to_original.py {directory}/starlink_ablation_selected4.tle")

        print(f"Cycle {i + 1} for satellite {i} completed with {base_name}.")

def main():
    source_files = [
        # ("starlink_ablation_source.tle", "original")
        ("starlink_ablation_diffheight.tle", "diffheight"),
        ("starlink_ablation_diffinclination_43.tle", "diffinclination"),
        ("starlink_ablation_diffphase.tle", "diffphase")
    ]

    for source_file, base_name in source_files:
        process_source_file(f"Ablation/{source_file}", base_name)

if __name__ == "__main__":
    main()
