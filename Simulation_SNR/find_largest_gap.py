import sys
import re
from datetime import timedelta

def parse_timedelta(time_str):
    days = 0
    if 'day' in time_str:
        days_part, time_str = time_str.split(', ')
        days = int(days_part.split(' ')[0])
    h, m, s = map(float, time_str.split(':'))
    return timedelta(days=days, hours=h, minutes=m, seconds=s)

def find_largest_gap(source_file, target_file):
    largest_gap = timedelta()
    largest_gap_info = ""

    with open(source_file, 'r') as file:
        for line in file:
            if "gap of" in line.lower():
                gap_duration = re.search(r"gap of ([\d:,.\s]+) found", line.lower()).group(1).strip()
                current_gap_duration = parse_timedelta(gap_duration)
                if current_gap_duration > largest_gap:
                    largest_gap = current_gap_duration
                    largest_gap_info = line.strip()

    if largest_gap_info:
        with open(target_file, 'a') as file:
            file.write(f"Largest {largest_gap_info}\n")
    else:
        print("No gaps found in the file.")

# Usage
if len(sys.argv) == 3:
    source_file = sys.argv[1]
    target_file = sys.argv[2]
    find_largest_gap(source_file, target_file)
else:
    print("Usage: python find_largest_gap.py source_file target_file")
