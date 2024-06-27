import subprocess
import os
import re
from datetime import timedelta

def parse_duration(duration_str):
    if duration_str == "0:00:00":
        return timedelta(seconds=0)
    if "day" in duration_str:
        days, time_str = duration_str.split(", ")
        days = int(days.split()[0])
        h, m, s = map(float, time_str.split(':'))
        return timedelta(days=days, hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))
    else:
        h, m, s = map(float, duration_str.split(':'))
        return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

def find_largest_gap(source_file, target_file):
    largest_gap = timedelta()
    largest_gap_info = ""

    with open(source_file, 'r') as file:
        for line in file:
            if "gap of" in line.lower():
                gap_duration = re.search(r"gap of ([\d:,.\s]+) found", line.lower()).group(1).strip()
                current_gap_duration = parse_duration(gap_duration)
                if current_gap_duration > largest_gap:
                    largest_gap = current_gap_duration
                    largest_gap_info = line.strip()

    if largest_gap_info:
        with open(target_file, 'a') as file:
            file.write(f"Largest {largest_gap_info}\n")
    else:
        print("No gaps found in the file.")

repetitions = int(input("Enter the number of repetitions: "))

folder_name = "NumSat_Taipei"
os.makedirs(folder_name, exist_ok=True)

numbers = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 3000]

for num in numbers:
    target_gap_duration_file = os.path.join(folder_name, f"total_gap_duration_analysis_{num}.txt")

    open(target_gap_duration_file, 'w').close()

    for rep in range(1, repetitions + 1):
        input_tle = os.path.join(folder_name, "imaging_num.tle")
        output_json = os.path.join(folder_name, f"output_file_{num}_random.json")
        output_txt = os.path.join(folder_name, f"output_{num}_random.txt")
        output_gaps_report_txt = os.path.join(folder_name, f"output_{num}_random_gaps_report_10001.txt")

        command1 = f"python3 change_tle.py starlink_original.tle {input_tle} {num}"
        command2 = f"python3 create_config_v2.py {input_tle} gs_tp.txt '2024-04-09 12:00:00' '2024-04-16 12:00:00' '1' {output_json}"
        command3 = f"python3 imagesatellite.py {output_json} > {output_txt}"
        command4 = f"python3 correct_lines_in_txt.py {output_txt}"
        command5 = f"python3 output_examine_v2.py {output_txt} '2024-04-09 12:00:00' '2024-04-16 12:00:00'"
        command6 = f"python3 find_largest_gap.py {output_gaps_report_txt} {target_gap_duration_file}"

        try:
            print(f"Running commands for number: {num}, repetition: {rep}")
            subprocess.run(command1, shell=True, check=True)
            subprocess.run(command2, shell=True, check=True)
            subprocess.run(command3, shell=True, check=True)
            subprocess.run(command4, shell=True, check=True)
            subprocess.run(command5, shell=True, check=True)
            subprocess.run(command6, shell=True, check=True)
            print(f"Completed commands for number: {num}, repetition: {rep}\n")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

print("Script completed.")
