import matplotlib.pyplot as plt
import os
import re
from datetime import timedelta
import numpy as np
import plot_config

def parse_gap_duration_file(file_path):
    total_durations = []
    with open(file_path, 'r') as file:
        for line in file:
            if "Total gap duration:" in line:
                total_gap_str = line.split("Total gap duration: ")[1].strip()
                total_durations.append(parse_duration(total_gap_str).total_seconds())
    if total_durations:
        return np.mean(total_durations)
    else:
        return 0

def parse_largest_gap_file(file_path):
    largest_gap = timedelta()
    with open(file_path, 'r') as file:
        for line in file:
            if "Largest Gap of" in line:
                largest_gap_str = re.search(r"Largest Gap of ([\d:,.\s]+) found", line).group(1).strip()
                current_gap = parse_duration(largest_gap_str).total_seconds()
                if current_gap > largest_gap.total_seconds():
                    largest_gap = timedelta(seconds=current_gap)
    return largest_gap.total_seconds()

def parse_duration(duration_str):
    if duration_str == "0:00:00":
        return timedelta(seconds=0)
    if "day" in duration_str:
        days, time_str = duration_str.split(", ")
        days = int(days.split()[0])
        h, m, s = map(float, time_str.split(':'))
        return timedelta(days=days, hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))
    else:
        h, m, s = map(float, duration_str.split(':'))
        return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

folder_path = "NumSat"
gap_duration_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.startswith('output_') and f.endswith('_random_gap_duration_analysis_10001.txt')]
largest_gap_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.startswith('total_gap_duration_analysis_') and f.endswith('.txt')]

data = {}
for file_path in gap_duration_files:
    num_satellites = int(re.search(r"output_(\d+)_random_gap_duration_analysis_10001.txt", file_path).group(1))
    avg_total_gap_duration = parse_gap_duration_file(file_path)
    data[num_satellites] = [avg_total_gap_duration, 0]

for file_path in largest_gap_files:
    num_satellites = int(re.search(r"total_gap_duration_analysis_(\d+).txt", file_path).group(1))
    largest_gap = parse_largest_gap_file(file_path)
    if num_satellites in data:
        data[num_satellites][1] = largest_gap
    else:
        data[num_satellites] = [0, largest_gap]

sorted_data = sorted(data.items())

for num_sat, (avg_total_gap_duration, largest_gap) in sorted_data:
    print(f"Number of Satellites: {num_sat}, Average Total Gap Duration: {avg_total_gap_duration:.2f} seconds, Largest Gap: {largest_gap:.2f} seconds")

fig, ax1 = plt.subplots(figsize=(10,6))
avg_total_gaps = [item[1][0] for item in sorted_data]
largest_gaps = [item[1][1] for item in sorted_data]

bar_width = 0.35
index = np.arange(len(sorted_data))

rects1 = ax1.bar(index - bar_width/2, avg_total_gaps, bar_width, color='blue', label='Average Total Gap Duration', hatch=plot_config.hatches[0], alpha=0.7)

ax2 = ax1.twinx()
rects2 = ax2.bar(index + bar_width/2, largest_gaps, bar_width, color='red', label='Largest Gap', hatch=plot_config.hatches[1], alpha=0.5)

ax1.set_xlabel('Number of Satellites')
ax1.set_ylabel('Average Total Gap Duration (seconds)', color='blue')
ax2.set_ylabel('Largest Gap (seconds)', color='red')
ax1.set_xticks(index)
ax1.set_xticklabels([item[0] for item in sorted_data])
ax1.tick_params(axis='y', labelcolor='blue')
ax2.tick_params(axis='y', labelcolor='red')

fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig('plot_gap_analysis_numsat.png')
print("Plot saved as 'plot_gap_analysis_numsat.png'")
