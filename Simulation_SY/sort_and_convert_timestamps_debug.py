import re
import sys
from datetime import datetime
from collections import defaultdict

# Function to convert Unix timestamp to human-readable format
def convert_unix_to_readable(unix_time):
    return datetime.utcfromtimestamp(float(unix_time)).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py input_file_path")
        sys.exit(1)

    input_file_path = sys.argv[1]
    base_file_name = input_file_path.rsplit('.', 1)[0]  # Removes the file extension

    # Regular expression to match the timestamps and nodeID accurately
    pattern = re.compile(r'nodeID: (\d+).*?startTimeUnix: (\d+(?:\.\d+)?).*?endTimeUnix: (\d+(?:\.\d+)?)')

    # Read the original output file
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Parse the lines to extract and convert timestamps
    entries_by_node = defaultdict(list)
    for line in lines:
        match = pattern.search(line)
        if match:
            nodeID, startTimeUnix, endTimeUnix = match.groups()
            entries_by_node[nodeID].append((float(startTimeUnix), float(endTimeUnix), line.strip()))

    # Sort entries by nodeID and then by startTimeUnix
    sorted_entries = []
    for nodeID, entries in entries_by_node.items():
        sorted_entries.extend(sorted(entries, key=lambda x: x[0]))

    # Create the output file with sorted entries
    sorted_output_file_path = f'{base_file_name}_sorted.txt'
    with open(sorted_output_file_path, 'w') as output_file:
        for entry in sorted_entries:
            nodeID = re.search(r'nodeID: (\d+)', entry[2]).group(1)
            start_time_readable = convert_unix_to_readable(entry[0])
            end_time_readable = convert_unix_to_readable(entry[1])
            output_line = re.sub(r'startTimeUnix: \d+(?:\.\d+)?', f'startTime: {start_time_readable}', entry[2])
            output_line = re.sub(r'endTimeUnix: \d+(?:\.\d+)?', f'endTime: {end_time_readable}', output_line)
            output_file.write(output_line + '\n')

    print(f"Sorted and formatted entries have been written to {sorted_output_file_path}")
