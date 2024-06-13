import re
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import os
import plot_config

def parse_duration(duration_str):
    h, m, s = map(float, duration_str.split(':'))
    return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

def analyze_file(filename):
    durations = []
    original_duration = None
    folder_path = "PlusOne"  

    full_path = os.path.join(folder_path, filename)  
    with open(full_path, 'r') as file:
        first_line = next(file)
        match = re.search(r'Total gap duration: (\d+:\d+:\d+\.\d+)', first_line)
        if match:
            original_duration = parse_duration(match.group(1))

        if not original_duration:
            return durations  

        for line in file:
            match = re.search(r'Total gap duration: (\d+:\d+:\d+\.\d+)', line)
            if match:
                duration = parse_duration(match.group(1))
                difference = abs(duration - original_duration)
                durations.append(difference.total_seconds())

    return durations

def format_seconds(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def main():
    files_info = [
        ('gap_duration_analysis_plus1_1.txt', "1 + 1"),
        ('gap_duration_analysis_plus1_100.txt', "100 + 1"),
        ('gap_duration_analysis_plus1_500.txt', "500 + 1")
    ]
    results = []
    errors = []
    min_max_values = []
    colors = plot_config.experiment_colors[:len(files_info)]
    hatches = plot_config.hatches[:len(files_info)]
    annotation_fontsize = plot_config.annotation_fontsize


    for filename, label in files_info:
        durations = analyze_file(filename)
        if durations:
            average_difference = np.mean(durations)
            min_difference = np.min(durations)
            max_difference = np.max(durations)
            results.append(average_difference)
            errors.append([average_difference - min_difference, max_difference - average_difference])
            min_max_values.append((min_difference, max_difference))
        else:
            results.append(0)  
            errors.append([0, 0])
            min_max_values.append((0, 0))

    fig, ax = plt.subplots()
    labels = [label for _, label in files_info]
    ax.bar(labels, results, yerr=np.array(errors).T, capsize=5, color=colors, hatch=hatches)
    ax.set_ylabel('Average Difference in Seconds')
    ax.set_xlabel('Base Number of Satellites (1, 100, 500)')
    # ax.set_title('Average Time Difference From Original Gaps')

    for i, (min_val, max_val) in enumerate(min_max_values):
        bar = ax.patches[i]
        bar_height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, bar_height + errors[i][1], f"Max: {format_seconds(max_val)}", ha='center', va='bottom', fontsize=annotation_fontsize)
        # ax.text(bar.get_x() + bar.get_width() / 2, bar_height - errors[i][0], f"Min: {format_seconds(min_val)}", ha='center', va='top', fontsize=annotation_fontsize)

    plt.savefig('plot_gap_duration_difference_plus1_min_max.png', dpi=300)

if __name__ == "__main__":
    main()
