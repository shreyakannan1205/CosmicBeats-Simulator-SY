import matplotlib.pyplot as plt
import os
import re
from datetime import timedelta
import numpy as np
import plot_config 

def parse_gap_report(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    gap_count = content.count("Gap of")

    total_gap_search = re.search(r"Total gap duration: (.+)", content)
    total_gap_duration = timedelta()
    if total_gap_search:
        total_gap_str = total_gap_search.group(1)
        h, m, s = map(float, total_gap_str.split(':'))
        total_gap_duration = timedelta(hours=h, minutes=m, seconds=s)

    gap_durations = re.findall(r"Gap of (.+?) found", content)
    largest_gap_duration = timedelta()
    for gap in gap_durations:
        h, m, s = map(float, gap.split(':'))
        current_gap_duration = timedelta(hours=h, minutes=m, seconds=float(s))
        if current_gap_duration > largest_gap_duration:
            largest_gap_duration = current_gap_duration

    return gap_count, total_gap_duration.total_seconds(), largest_gap_duration.total_seconds()

folder_path = "NumSat"
file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('_gaps_report.txt')]

data = {}
for file_path in file_names:
    num_satellites = int(re.search(r"(\d+)", file_path).group(1))
    gap_count, total_gap_duration, largest_gap_duration = parse_gap_report(file_path)
    data[num_satellites] = (gap_count, total_gap_duration, largest_gap_duration)

sorted_data = sorted(data.items())

for num_sat, info in sorted_data:
    gap_count, total_gap_duration, largest_gap_duration = info
    print(f"Number of Satellites: {num_sat}, Total Gap Duration: {total_gap_duration:.2f}, Largest Gap: {largest_gap_duration:.2f}")

fig2, ax2 = plt.subplots(figsize=(10,6))
total_gaps = [item[1][1] for item in sorted_data]
largest_gaps = [item[1][2] for item in sorted_data]

bar_width = 0.35
index = np.arange(len(sorted_data))

rects1 = ax2.bar(index - bar_width/2, total_gaps, bar_width, color='blue', label='Total Gap Duration', hatch=plot_config.hatches[0], alpha=0.7)

ax3 = ax2.twinx()
rects2 = ax3.bar(index + bar_width/2, largest_gaps, bar_width, color='red', label='Largest Gap', alpha=0.5, hatch=plot_config.hatches[1])

ax2.set_xlabel('Number of Satellites')
ax2.set_ylabel('Total Gap Duration (seconds)', color='blue')
ax3.set_ylabel('Largest Gap (seconds)', color='red')
ax2.set_xticks(index)
ax2.set_xticklabels([item[0] for item in sorted_data])
ax2.tick_params(axis='y', labelcolor='blue')
ax3.tick_params(axis='y', labelcolor='red')

ax2.legend(loc='upper left')
ax3.legend(loc='upper right')

fig2.tight_layout()  
# plt.title('Satellite Communication Gap Analysis - 24h period', fontsize=plot_config.xyfontsize)
plt.savefig('plot_gap_analysis_numsat.png')  
# plt.show()
