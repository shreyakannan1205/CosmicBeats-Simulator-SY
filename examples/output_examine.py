import re
from datetime import datetime, timedelta

# Function to convert Unix timestamp to human-readable format
def convert_unix_to_readable(unix_time):
    return datetime.utcfromtimestamp(float(unix_time)).strftime('%Y-%m-%d %H:%M:%S')

# Regular expression to match the timestamps accurately
timestamp_pattern = re.compile(r'startTimeUnix: (\d+(?:\.\d+)?).*?endTimeUnix: (\d+(?:\.\d+)?)')

# Read the original output file
with open('output_100_random.txt', 'r') as file:
    lines = file.readlines()

# Parse the lines to extract and convert timestamps
entries = []
for line in lines:
    match = timestamp_pattern.search(line)
    if match:
        startTimeUnix, endTimeUnix = match.groups()
        entries.append((float(startTimeUnix), float(endTimeUnix), line.strip()))

# Sort the entries by the start time
entries.sort(key=lambda x: x[0])

# Save the sorted entries to a new file
with open('sorted_logs_100_random.txt', 'w') as sorted_file:
    for entry in entries:
        sorted_file.write(f"{entry[2]}\n")

# Initialize total gap duration
total_gap_duration = timedelta(seconds=0)

# Open a file to write the gap logs
with open('gaps_report_100_random.txt', 'w') as report_file:
    # Find, report, and sum up the durations of gaps larger than 1 second
    for i in range(1, len(entries)):
        prev_entry = entries[i - 1]
        current_entry = entries[i]
        gap = current_entry[0] - prev_entry[1]  # Calculate the gap
        if gap > 1:
            gap_duration = timedelta(seconds=gap)
            total_gap_duration += gap_duration
            gap_info = f"Gap of {gap_duration} found between {convert_unix_to_readable(prev_entry[1])} and {convert_unix_to_readable(current_entry[0])}\n"
            print(gap_info, end='')  # Print to console
            report_file.write(gap_info)  # Write to file

    # Print and write the total duration of all gaps
    total_gap_info = f"Total gap duration: {total_gap_duration}\n"
    print(total_gap_info, end='')
    report_file.write(total_gap_info)
