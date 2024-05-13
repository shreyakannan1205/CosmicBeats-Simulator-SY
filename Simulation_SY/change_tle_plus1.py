import random
import sys

def pick_random_satellite(source_file, target_file, log_file):
    with open(source_file, 'r') as file:
        lines = file.readlines()

    # Group lines into sets of three (each satellite's data)
    satellites = [lines[i:i+3] for i in range(0, len(lines), 3)]

    # Randomly select one satellite
    selected_satellite = random.choice(satellites)

    # Print selected satellite data to console and log to a file
    print("Selected satellite data:")
    for line in selected_satellite:
        print(line.strip())
        with open(log_file, 'a') as log:
            log.write(line)

    # Write the selected satellite's data to the target file
    with open(target_file, 'a') as file:
        file.writelines(selected_satellite)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <source_file> <target_file> <log_file>")
    else:
        source_file = sys.argv[1]
        target_file = sys.argv[2]
        log_file = sys.argv[3]
        pick_random_satellite(source_file, target_file, log_file)
