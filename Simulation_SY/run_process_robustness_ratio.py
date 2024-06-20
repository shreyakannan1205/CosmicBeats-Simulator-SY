import subprocess
import os

def run_script(command):
    """Helper function to run a shell command."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def run_initial_scripts(directory, source_file, base_name):
    print(f"Running initial analysis on {source_file} with {base_name} sats.")
    run_script(f"python3 create_config_v2.py {source_file} gs.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_robustness_ratio_{base_name}.json")
    run_script(f"python3 imagesatellite.py {directory}/output_robustness_ratio_{base_name}.json > {directory}/output_robustness_ratio_{base_name}.txt")
    run_script(f"python3 correct_lines_in_txt.py {directory}/output_robustness_ratio_{base_name}.txt")
    run_script(f"python3 output_examine_v2.py {directory}/output_robustness_ratio_{base_name}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")

def run_repetitive_tasks(directory, source_file, base_name, repetitions, denied_numbers, labels):
    for denied, label in zip(denied_numbers, labels):
        for i in range(repetitions):
            print(f"Cycle {i + 1} with {denied} denied starts with {base_name} (label: {label}).")
            run_script(f"python3 change_tle_robustness.py {source_file} {directory}/imaging_{base_name}.tle {denied}")
            run_script(f"python3 create_config_v2.py {directory}/imaging_{base_name}.tle gs.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_robustness_ratio_{base_name}_{label}.json")
            run_script(f"python3 imagesatellite.py {directory}/output_robustness_ratio_{base_name}_{label}.json > {directory}/output_robustness_ratio_{base_name}_{label}.txt")
            run_script(f"python3 correct_lines_in_txt.py {directory}/output_robustness_ratio_{base_name}_{label}.txt")
            run_script(f"python3 output_examine_v2.py {directory}/output_robustness_ratio_{base_name}_{label}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
            print(f"Cycle {i + 1} with {denied} denied completed for {base_name} (label: {label}).")

def main():
    directory = "Robustness_Ratio"
    os.makedirs(directory, exist_ok=True)

    source_files = [
        ("starlink_original_totalsize_1000.tle", "1000")
    ]

    repetitions = int(input("Enter the number of repetitions: "))
    denied_numbers = [91, 167, 230, 286, 334, 375, 412, 444, 474, 500]
    labels = [f"{i}_1" for i in range(1, 11)]

    for source_file, base_name in source_files:
        run_initial_scripts(directory, source_file, base_name)
        run_repetitive_tasks(directory, source_file, base_name, repetitions, denied_numbers, labels)

if __name__ == "__main__":
    main()
