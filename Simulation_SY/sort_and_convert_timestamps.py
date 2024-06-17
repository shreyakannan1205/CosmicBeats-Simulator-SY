import re
import sys
import glob
from datetime import datetime
import os

# Function to convert Unix timestamp to human-readable format
def convert_unix_to_readable(unix_time):
    return datetime.utcfromtimestamp(float(unix_time)).strftime('%Y-%m-%d %H:%M:%S')

def is_useless_interval(interval, intervals):
    start, end = interval
    for other_start, other_end in intervals:
        if other_start <= start and other_end >= end and (other_start != start or other_end != end):
            return True
    return False

def get_useless_intervals_ratio(intervals):
    useless_intervals_count = sum(is_useless_interval(interval, intervals) for interval in intervals)
    total_intervals = len(intervals)
    useless_ratio = useless_intervals_count / total_intervals
    return useless_ratio, [interval for interval in intervals if is_useless_interval(interval, intervals)]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 process_multiple_files.py summary_file_path")
        sys.exit(1)

    summary_file_path = sys.argv[1]
    input_file_pattern = os.path.join("NumSat", "output_*_random.txt")  # Pattern for input files in the NumSat directory

    # Get a list of all input files matching the pattern
    input_files = glob.glob(input_file_pattern)

    with open(summary_file_path, 'w') as summary_file:
        for input_file_path in input_files:
            output_file_path = input_file_path.replace('.txt', '_sorted.txt')

            # Regular expression to match the timestamps accurately
            timestamp_pattern = re.compile(r'Pass\. nodeID: (\d+)\. nodeType: (\d+)\. startTimeUnix: (\d+(?:\.\d+)?)\. endTimeUnix: (\d+(?:\.\d+)?)')

            # Read the original output file
            with open(input_file_path, 'r') as file:
                lines = file.readlines()

            # Parse the lines to extract and convert timestamps
            entries = []
            for line in lines:
                match = timestamp_pattern.search(line)
                if match:
                    nodeID, nodeType, startTimeUnix, endTimeUnix = match.groups()
                    startTimeUnix = float(startTimeUnix)
                    endTimeUnix = float(endTimeUnix)
                    entries.append((startTimeUnix, endTimeUnix, nodeID, nodeType, line.strip()))

            # Sort the entries by the start time
            entries.sort(key=lambda x: x[0])

            # Extract intervals for useless interval calculation
            intervals = [(entry[0], entry[1]) for entry in entries]
            useless_ratio, useless_intervals = get_useless_intervals_ratio(intervals)

            # Write the sorted and formatted entries to the output file
            with open(output_file_path, 'w') as file:
                file.write("[Simulator Info] Computing FOVs...\n")
                for entry in entries:
                    start_time_readable = convert_unix_to_readable(entry[0])
                    end_time_readable = convert_unix_to_readable(entry[1])
                    is_useless = (entry[0], entry[1]) in useless_intervals
                    formatted_line = f"Pass. nodeID: {entry[2]}. nodeType: {entry[3]}. startTime: {start_time_readable}. endTime: {end_time_readable}"
                    if is_useless:
                        formatted_line += " USELESS"
                    file.write(formatted_line + "\n")

            # Append the result to the summary file
            summary_file.write(f"{input_file_path}: Useless timestamp ratio: {useless_ratio:.2f}\n")

            print(f"Processed {input_file_path}, saved to {output_file_path}, Useless timestamp ratio: {useless_ratio:.2f}")

    print(f"Summary of useless timestamp ratios saved to {summary_file_path}")
