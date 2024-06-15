import subprocess
import os

def run_script(command):
    """ Helper function to run a shell command. """
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def process_source_file(directory, city, gs_file, number, repetitions):
    # Initial script to process with different numbers
    run_script(f"python3 change_tle_initial.py starlink_original.tle {directory}/imaging_plus1.tle {directory}/starlink_plus1.tle {number}")
    run_script(f"python3 create_config.py {directory}/imaging_plus1.tle {gs_file} '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_plus1_{number}_{city}.json")
    run_script(f"python3 imagesatellite.py {directory}/output_plus1_{number}_{city}.json > {directory}/output_plus1_{number}_{city}.txt")
    run_script(f"python3 output_examine.py {directory}/output_plus1_{number}_{city}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
    run_script(f"python3 gap_duration_analysis.py {directory}/output_plus1_{number}_{city}_gaps_report.txt {directory}/gap_duration_analysis_plus1_{number}_{city}.txt")

    for i in range(repetitions):
        print(f"Cycle {i + 1} for number {number} in city {city} starts.")

        # Run scripts with dynamically generated file names based on the current number, cycle, and city
        run_script(f"python3 change_tle_plus1.py {directory}/starlink_plus1.tle {directory}/imaging_plus1.tle {directory}/gap_duration_analysis_plus1_{number}_{city}.txt")
        run_script(f"python3 create_config.py {directory}/imaging_plus1.tle {gs_file} '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_plus1_{number}_{city}.json")
        run_script(f"python3 imagesatellite.py {directory}/output_plus1_{number}_{city}.json > {directory}/output_plus1_{number}_{city}.txt")
        run_script(f"python3 output_examine.py {directory}/output_plus1_{number}_{city}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
        run_script(f"python3 gap_duration_analysis.py {directory}/output_plus1_{number}_{city}_gaps_report.txt {directory}/gap_duration_analysis_plus1_{number}_{city}.txt")
        run_script(f"python3 change_tle_to_original.py {directory}/imaging_plus1.tle")

        print(f"Cycle {i + 1} for number {number} in city {city} completed.")

def main():
    directory = "PlusOne"
    os.makedirs(directory, exist_ok=True)

    ground_stations = [
        ("gs/gs_tw.txt", "taipei"),
        ("gs/gs_ny.txt", "ny"),
        ("gs/gs_sp.txt", "saopaulo"),
        ("gs/gs_mum.txt", "mumbai"),
        ("gs/gs_la.txt", "la"),
        ("gs/gs_lg.txt", "lagos"),
        ("gs/gs_mos.txt", "moscow"),
        ("gs/gs_sy.txt", "sydney"),
        ("gs/gs_sk.txt", "seoul"),
        ("gs/gs_pa.txt", "paris")
    ]

    try:
        numbers = list(map(int, input("Enter the numbers separated by space (First try was 1 100 500): ").split()))
    except ValueError:
        print("Invalid input. Please enter valid integers separated by spaces.")
        return  

    # Ask for the number of repetitions at the start to be used for all numbers
    try:
        repetitions = int(input("Enter the number of repetitions for all numbers: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for the number of repetitions.")
        return  

    for gs_file, city in ground_stations:
        for number in numbers:
            process_source_file(directory, city, gs_file, number, repetitions)

if __name__ == "__main__":
    main()
