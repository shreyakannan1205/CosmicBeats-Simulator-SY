import subprocess
import os

def run_script(command):
    """ Helper function to run a shell command. """
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def process_source_file(source_file, base_name, repetitions, denied_numbers, labels):
    directory = "Resilience"
    os.makedirs(directory, exist_ok=True)

    # Run the initial set of scripts on the source file
    print(f"Running initial analysis on {source_file} with {base_name}.")
    run_script(f"python3 create_config.py {source_file} gs.txt '2024-04-09 12:00:00' '2024-04-10 12:00:00' '1' {directory}/output_initial_ratio_{base_name}.json")
    run_script(f"python3 imagesatellite.py {directory}/output_initial_ratio_{base_name}.json > {directory}/output_initial_ratio_{base_name}.txt")
    run_script(f"python3 output_examine.py {directory}/output_initial_ratio_{base_name}.txt")
    run_script(f"python3 gap_duration_analysis.py {directory}/output_initial_ratio_{base_name}_gaps_report.txt {directory}/gap_duration_analysis_initial_ratio_{base_name}.txt")

    # Iterate over the denied numbers and run the repetitions for each
    for denied, label in zip(denied_numbers, labels):
        for i in range(repetitions):
            print(f"Cycle {i + 1} with {denied} denied starts with {base_name} (label: {label}).")
            run_script(f"python3 change_tle_resilience.py {source_file} {directory}/imaging_{base_name}.tle {denied}")
            run_script(f"python3 create_config.py {directory}/imaging_{base_name}.tle gs.txt '2024-04-09 12:00:00' '2024-04-10 12:00:00' '1' {directory}/output_resilience_{base_name}_{label}.json")
            run_script(f"python3 imagesatellite.py {directory}/output_resilience_{base_name}_{label}.json > {directory}/output_resilience_{base_name}_{label}.txt")
            run_script(f"python3 output_examine.py {directory}/output_resilience_{base_name}_{label}.txt")
            run_script(f"python3 gap_duration_analysis.py {directory}/output_resilience_{base_name}_{label}_gaps_report.txt {directory}/gap_duration_analysis_resilience_{base_name}_{label}.txt")

            print(f"Cycle {i + 1} with {denied} denied completed for {base_name} (label: {label}).")

def main():
    source_files = [
        ("starlink_original_totalsize_1000.tle", "1000")
    ]
    
    repetitions = int(input("Enter the number of repetitions: "))
    denied_numbers = [91, 167, 230, 286, 334, 375, 412, 444, 474, 500]
    labels = [f"{i}_1" for i in range(1, 11)]

    for source_file, base_name in source_files:
        process_source_file(f"Resilience/{source_file}", base_name, repetitions, denied_numbers, labels)

if __name__ == "__main__":
    main()
