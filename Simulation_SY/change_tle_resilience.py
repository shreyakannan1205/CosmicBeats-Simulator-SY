import random
import sys

def erase_random_satellites(source_file, target_file, num_to_erase):
    with open(source_file, 'r') as file:
        lines = file.readlines()

    satellites = [lines[i:i+3] for i in range(0, len(lines), 3)]

    if num_to_erase > len(satellites):
        print(f"Cannot erase {num_to_erase} satellites. The file only contains {len(satellites)} satellites.")
        return

    selected_satellites = random.sample(satellites, num_to_erase)

    remaining_satellites = [sat for sat in satellites if sat not in selected_satellites]

    with open(target_file, 'w') as file:
        for satellite in remaining_satellites:
            file.writelines(satellite)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 change_tle_resilience.py <source_file> <target_file> <num_to_erase>")
    else:
        source_file = sys.argv[1]
        target_file = sys.argv[2]
        num_to_erase = int(sys.argv[3])
        erase_random_satellites(source_file, target_file, num_to_erase)
