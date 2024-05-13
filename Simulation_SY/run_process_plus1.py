import subprocess
import os

def run_script(command):
    """ Helper function to run a shell command. """
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def main():
    # Create or check the 'PlusOne' directory
    directory = "PlusOne"
    os.makedirs(directory, exist_ok=True)

    # Ask user for the numbers list
    try:
        numbers = list(map(int, input("Enter the numbers separated by space (First try was 1 100 500): ").split()))
    except ValueError:
        print("Invalid input. Please enter valid integers separated by spaces.")
        return  # Exit if input is not valid integers

    # Ask for the number of repetitions at the start to be used for all numbers
    try:
        repetitions = int(input("Enter the number of repetitions for all numbers: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for the number of repetitions.")
        return  # Exit if the repetition input is not valid

    for number in numbers:
        # Initial script to process with different numbers, adjusted to use the 'PlusOne' directory
        run_script(f"python3 change_tle_initial.py starlink_original.tle {directory}/imaging_plus1.tle {directory}/starlink_plus1.tle {number}")
        run_script(
            f"python3 create_config.py {directory}/imaging_plus1.tle gs.txt '2024-04-09 12:00:00' '2024-04-10 12:00:00' '1' {directory}/output_plus1_{number}.json")
        run_script(f"python3 imagesatellite.py {directory}/output_plus1_{number}.json > {directory}/output_plus1_{number}.txt")
        run_script(f"python3 output_examine.py {directory}/output_plus1_{number}.txt")
        run_script(
            f"python3 gap_duration_analysis.py {directory}/output_plus1_{number}_gaps_report.txt {directory}/gap_duration_analysis_plus1_{number}.txt")

        for i in range(repetitions):
            print(f"Cycle {i + 1} for number {number} starts.")

            # Run scripts with dynamically generated file names based on the current number and cycle, adjusted to use the 'PlusOne' directory
            run_script(f"python3 change_tle_plus1.py {directory}/starlink_plus1.tle {directory}/imaging_plus1.tle {directory}/gap_duration_analysis_plus1_{number}.txt")
            run_script(f"python3 create_config.py {directory}/imaging_plus1.tle gs.txt '2024-04-09 12:00:00' '2024-04-10 12:00:00' '1' {directory}/output_plus1_{number}.json")
            run_script(f"python3 imagesatellite.py {directory}/output_plus1_{number}.json > {directory}/output_plus1_{number}.txt")
            run_script(f"python3 output_examine.py {directory}/output_plus1_{number}.txt")
            run_script(f"python3 gap_duration_analysis.py {directory}/output_plus1_{number}_gaps_report.txt {directory}/gap_duration_analysis_plus1_{number}.txt")
            run_script(f"python3 change_tle_to_original.py {directory}/imaging_plus1.tle")

            print(f"Cycle {i + 1} for number {number} completed.")

if __name__ == "__main__":
    main()
