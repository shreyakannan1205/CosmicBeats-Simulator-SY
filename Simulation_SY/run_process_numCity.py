import subprocess
import os

def run_script(command):
    """ Helper function to run a shell command. """
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def extract_top_n_lines(input_file, output_file, n):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        with open(output_file, 'w') as outfile:
            outfile.writelines(lines[:n])
    except Exception as e:
        print(f"An error occurred while extracting lines: {e}")

def process_source_file(source_file, gs_file):
    with open(gs_file, 'r') as file:
        lines = file.readlines()
    
    num_lines = len(lines)
    directory = "NumCity"
    os.makedirs(directory, exist_ok=True)

    for n in range(1, num_lines + 1):
        gs_n_file = f"{directory}/gs_{n}.txt"
        extract_top_n_lines(gs_file, gs_n_file, n)

        run_script(f"python3 create_config_v2.py {source_file} {gs_n_file} '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {directory}/output_numcity_{n}.json")
        run_script(f"python3 imagesatellite.py {directory}/output_numcity_{n}.json > {directory}/output_numcity_{n}.txt")
        run_script(f"python3 correct_lines_in_txt.py {directory}/output_numcity_{n}.txt")
        run_script(f"python3 output_examine_v2.py {directory}/output_numcity_{n}.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00'")

def main():
    source_file = "imaging_1.tle"
    gs_file = "gs.txt"

    process_source_file(source_file, gs_file)

if __name__ == "__main__":
    main()
