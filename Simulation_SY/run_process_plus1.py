import subprocess
import os

def run_script(command):
    """ Helper function to run a shell command. """
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def process_source_file(directory, number, repetitions):
    # Run initial gap duration analysis
    run_script(f"python3 change_tle_initial.py starlink_original.tle {directory}/imaging_plus1_{number}.tle {directory}/starlink_plus1_{number}.tle {number}")
    run_script(f"python3 create_config_v2.py {directory}/imaging_plus1_{number}.tle gs.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_plus1_{number}.json")
    run_script(f"python3 imagesatellite.py {directory}/output_plus1_{number}.json > {directory}/output_plus1_{number}.txt")
    run_script(f"python3 correct_lines_in_txt.py {directory}/output_plus1_{number}.txt")
    run_script(f"python3 output_examine_v2.py {directory}/output_plus1_{number}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")

    for i in range(repetitions):
        print(f"Cycle {i + 1} for number {number} starts.")

        run_script(f"python3 change_tle_plus1.py {directory}/starlink_plus1_{number}.tle {directory}/imaging_plus1_{number}.tle {directory}/selected_satellite_list_{number}.txt")
        run_script(f"python3 create_config_v2.py {directory}/imaging_plus1_{number}.tle gs.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_plus1_{number}.json")
        run_script(f"python3 imagesatellite.py {directory}/output_plus1_{number}.json > {directory}/output_plus1_{number}.txt")
        run_script(f"python3 correct_lines_in_txt.py {directory}/output_plus1_{number}.txt")
        run_script(f"python3 output_examine_v2.py {directory}/output_plus1_{number}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")
        run_script(f"python3 change_tle_to_original.py {directory}/imaging_plus1_{number}.tle")

        print(f"Cycle {i + 1} for number {number} completed.")

def main():
    directory = "PlusOne_1002"
    os.makedirs(directory, exist_ok=True)

    try:
        numbers = list(map(int, input("Enter the numbers separated by space (First try was 1 100 500): ").split()))
    except ValueError:
        print("Invalid input. Please enter valid integers separated by spaces.")
        return  

    try:
        repetitions = int(input("Enter the number of repetitions for all numbers: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for the number of repetitions.")
        return  

    for number in numbers:
        process_source_file(directory, number, repetitions)

if __name__ == "__main__":
    main()
