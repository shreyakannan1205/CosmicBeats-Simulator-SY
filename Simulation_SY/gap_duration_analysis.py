import sys

def append_gap_duration(source_file, target_file):
    total_gap_duration = None

    with open(source_file, 'r') as file:
        for line in file:
            if line.startswith("Total gap duration:"):
                total_gap_duration = line.strip()
                break

    if total_gap_duration:
        with open(target_file, 'a') as file:
            file.write(total_gap_duration + '\n')
    else:
        print("Total gap duration not found in the file.")

# Usage
if len(sys.argv) == 3:
    source_file = sys.argv[1]
    target_file = sys.argv[2]
    append_gap_duration(source_file, target_file)
else:
    print("Usage: python gap_duration_analysis.py source_file target_file")
