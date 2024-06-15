import re
import sys
from datetime import datetime, timedelta
import pytz

# Function to convert Unix timestamp to human-readable format
def convert_unix_to_readable(unix_time):
    return datetime.utcfromtimestamp(float(unix_time)).strftime('%Y-%m-%d %H:%M:%S')

# Function to convert human-readable date to Unix timestamp
def convert_readable_to_unix(date_str):
    naive_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    utc_datetime = naive_datetime.replace(tzinfo=pytz.utc)
    return utc_datetime.timestamp()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py input_file_path initial_time_str final_time_str")
        sys.exit(1)

    input_file_path = sys.argv[1]
    initial_time_str = sys.argv[2]
    final_time_str = sys.argv[3]
    
    base_file_name = input_file_path.rsplit('.', 1)[0]  # Removes the file extension

    # Regular expression to match the timestamps accurately
    timestamp_pattern = re.compile(r'startTimeUnix: (\d+(?:\.\d+)?).*?endTimeUnix: (\d+(?:\.\d+)?)')

    # Read the original output file
    with open(input_file_path, 'r') as file:
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

    # Initialize total gap duration and largest gap details
    total_gap_duration = timedelta(seconds=0)
    largest_gap = timedelta(seconds=0)
    largest_gap_details = None

    # Convert initial and final times to Unix
    initial_time_unix = convert_readable_to_unix(initial_time_str)
    final_time_unix = convert_readable_to_unix(final_time_str)

    # Open a file to write the gap logs
    gaps_report_file_path = f'{base_file_name}_gaps_report.txt'
    with open(gaps_report_file_path, 'w') as report_file:
        # Initial gap
        if entries:
            initial_gap = entries[0][0] - initial_time_unix
            if initial_gap > 1:
                initial_gap_duration = timedelta(seconds=initial_gap)
                total_gap_duration += initial_gap_duration
                initial_gap_info = f"Initial gap of {initial_gap_duration} found between {initial_time_str} and {convert_unix_to_readable(entries[0][0])}\n"
                report_file.write(initial_gap_info)

        # Find, report, and sum up the durations of gaps larger than 1 second
        for i in range(1, len(entries)):
            prev_entry = entries[i - 1]
            current_entry = entries[i]
            gap = current_entry[0] - prev_entry[1]
            if gap > 1:
                gap_duration = timedelta(seconds=gap)
                total_gap_duration += gap_duration
                if gap_duration > largest_gap:
                    largest_gap = gap_duration
                    largest_gap_details = (prev_entry, current_entry)
                gap_info = f"Gap of {gap_duration} found between {convert_unix_to_readable(prev_entry[1])} and {convert_unix_to_readable(current_entry[0])}\n"
                report_file.write(gap_info)

        # Final gap
        if entries:
            final_gap = final_time_unix - entries[-1][1]
            if final_gap > 1:
                final_gap_duration = timedelta(seconds=final_gap)
                total_gap_duration += final_gap_duration
                final_gap_info = f"Final gap of {final_gap_duration} found between {convert_unix_to_readable(entries[-1][1])} and {final_time_str}\n"
                report_file.write(final_gap_info)

        # Write the total duration of all gaps
        total_gap_info = f"Total gap duration: {total_gap_duration}\n"
        report_file.write(total_gap_info)

        # # Write the largest gap details
        # if largest_gap_details:
        #     largest_gap_info = f"Largest gap of {largest_gap} found between {convert_unix_to_readable(largest_gap_details[0][1])} and {convert_unix_to_readable(largest_gap_details[1][0])}\n"
        #     report_file.write(largest_gap_info)

    # Print the total and largest gap info to console for confirmation
    print(total_gap_info, end='')
    # if largest_gap_details:
    #     print(largest_gap_info, end='')
