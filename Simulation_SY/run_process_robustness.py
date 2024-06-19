import subprocess
import os

def run_script(command):
    """ Helper function to run a shell command. """
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def process_source_file(directory, source_file, base_name, repetitions):
    # Run initial gap duration analysis
    print(f"Running initial analysis on {source_file} with {base_name} sats.")
    run_script(f"python3 create_config_v2.py {source_file} gs.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_robustness_{base_name}.json")
    run_script(f"python3 imagesatellite.py {directory}/output_robustness_{base_name}.json > {directory}/output_robustness_{base_name}.txt")
    run_script(f"python3 correct_lines_in_txt.py {directory}/output_robustness_{base_name}.txt")
    run_script(f"python3 output_examine_v2.py {directory}/output_robustness_{base_name}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
    
    for i in range(repetitions):
        print(f"Cycle {i + 1} starts with {base_name} sats.")
        run_script(f"python3 change_tle_robustness.py {source_file} {directory}/imaging_{base_name}.tle {int(base_name) // 2}")
        run_script(f"python3 create_config_v2.py {directory}/imaging_{base_name}.tle gs.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_robustness_{base_name}.json")
        run_script(f"python3 imagesatellite.py {directory}/output_robustness_{base_name}.json > {directory}/output_robustness_{base_name}.txt")
        run_script(f"python3 correct_lines_in_txt.py {directory}/output_robustness_{base_name}.txt")
        run_script(f"python3 output_examine_v2.py {directory}/output_robustness_{base_name}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
        print(f"Cycle {i + 1} completed with {base_name} sats.")

def main():
    directory = "Robustness"
    os.makedirs(directory, exist_ok=True)

    source_files = [
        ("starlink_original_totalsize_200.tle", "200"),
        ("starlink_original_totalsize_500.tle", "500"),
        ("starlink_original_totalsize_1000.tle", "1000"),
        ("starlink_original_totalsize_2000.tle", "2000")
    ]
    
    repetitions = int(input("Enter the number of repetitions: "))

    for source_file, base_name in source_files:
        process_source_file(directory, source_file, base_name, repetitions)

if __name__ == "__main__":
    main()
