import matplotlib.pyplot as plt
import os
import re
from datetime import timedelta
import numpy as np

plt.rc('font', size=18)  # Adjust font size for readability

def parse_gap_report(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Find the number of gaps
    gap_count = content.count("Gap of")

    # Extract total gap duration
    total_gap_search = re.search(r"Total gap duration: (.+)", content)
    total_gap_duration = timedelta()
    if total_gap_search:
        total_gap_str = total_gap_search.group(1)
        h, m, s = map(float, total_gap_str.split(':'))
        total_gap_duration = timedelta(hours=h, minutes=m, seconds=s)

    # Compute the largest gap by iterating over all gap entries
    gap_durations = re.findall(r"Gap of (.+?) found", content)
    largest_gap_duration = timedelta()
    for gap in gap_durations:
        h, m, s = map(float, gap.split(':'))
        current_gap_duration = timedelta(hours=h, minutes=m, seconds=float(s))
        if current_gap_duration > largest_gap_duration:
            largest_gap_duration = current_gap_duration

    return gap_count, total_gap_duration.total_seconds(), largest_gap_duration.total_seconds()

# Assuming files are stored in a folder named 'NumSat'
folder_path = "NumSat"
file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('_gaps_report.txt')]

# Extracting information from each file
data = {}
for file_path in file_names:
    # Extract the number of satellites from the file name
    num_satellites = int(re.search(r"(\d+)", file_path).group(1))
    gap_count, total_gap_duration, largest_gap_duration = parse_gap_report(file_path)
    data[num_satellites] = (gap_count, total_gap_duration, largest_gap_duration)

# Sort data by number of satellites
sorted_data = sorted(data.items())

# Print total gap duration sorted by number of satellites
for num_sat, info in sorted_data:
    gap_count, total_gap_duration, largest_gap_duration = info
    print(f"Number of Satellites: {num_sat}, Total Gap Duration: {total_gap_duration:.2f}, Largest Gap: {largest_gap_duration:.2f}")

# Plot 2: Total Gap Duration and Largest Gap
fig2, ax2 = plt.subplots(figsize=(20, 10))
total_gaps = [item[1][1] for item in sorted_data]
largest_gaps = [item[1][2] for item in sorted_data]

bar_width = 0.35
index = np.arange(len(sorted_data))

# Create the bar for Total Gap Duration on the primary y-axis
rects1 = ax2.bar(index - bar_width/2, total_gaps, bar_width, color='blue', label='Total Gap Duration (s)')

# Create an additional y-axis for the Largest Gap
ax3 = ax2.twinx()
# Create the bar for Largest Gap on the secondary y-axis
rects2 = ax3.bar(index + bar_width/2, largest_gaps, bar_width, color='red', label='Largest Gap (s)', alpha=0.6)

ax2.set_xlabel('Number of Satellites')
ax2.set_ylabel('Total Gap Duration (seconds)', color='blue')
ax3.set_ylabel('Largest Gap (seconds)', color='red')
ax2.set_xticks(index)
ax2.set_xticklabels([item[0] for item in sorted_data])
ax2.tick_params(axis='y', labelcolor='blue')
ax3.tick_params(axis='y', labelcolor='red')

fig2.tight_layout()  # Adjust layout to make room for the legend
ax2.legend(loc='upper left')
ax3.legend(loc='upper right')
plt.subplots_adjust(top=0.95)  # Adjust the top margin; increase the value if the title is cut off
plt.title('Satellite Communication Gap Analysis - 24h period')
plt.savefig('plot_gap_analysis.png')  # Save the plot as a PNG file
# plt.show()
