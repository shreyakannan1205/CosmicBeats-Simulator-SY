import random

def pick_random_satellite(source_file, target_file, log_file1, log_file2):
    with open(source_file, 'r') as file:
        lines = file.readlines()

    # Group lines into sets of three (each satellite's data)
    satellites = [lines[i:i+3] for i in range(0, len(lines), 3)]

    # Randomly select one satellite
    selected_satellite = random.choice(satellites)

    # Print selected satellite to console and log to a file
    print("Selected satellite data:")
    for line in selected_satellite:
        print(line.strip())
        with open(log_file1, 'a') as log:
            log.write(line)
        with open(log_file2, 'a') as log:
            log.write(line)

    # Write the selected satellite's data to the target file
    with open(target_file, 'a') as file:
        file.writelines(selected_satellite)

# Usage
pick_random_satellite('starlink.tle', 'imaging_sk_tw.tle', 'gap_duration_analysis_sk.txt', 'gap_duration_analysis_tw.txt')
