import re
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import os

def parse_duration(duration_str):
    h, m, s = map(float, duration_str.split(':'))
    return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

def analyze_file(filename):
    durations = []
    original_duration = None
    folder_path = "PlusOne"  # Define the folder where files are stored

    full_path = os.path.join(folder_path, filename)  # Generate the full path to the file
    with open(full_path, 'r') as file:
        first_line = next(file)
        match = re.search(r'Total gap duration: (\d+:\d+:\d+\.\d+)', first_line)
        if match:
            original_duration = parse_duration(match.group(1))

        if not original_duration:
            return durations  # Return empty list if original duration is not found

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
        ('gap_duration_analysis_plus1_1.txt', "1 plus one"),
        ('gap_duration_analysis_plus1_100.txt', "100 plus one"),
        ('gap_duration_analysis_plus1_500.txt', "500 plus one")
    ]
    results = []
    errors = []
    min_max_values = []
    colors = ['blue', 'green', 'red']  # List of colors for each bar

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
            results.append(0)  # Assuming zero difference if no durations found
            errors.append([0, 0])
            min_max_values.append((0, 0))

    # Plotting the results with error bars
    fig, ax = plt.subplots()
    labels = [label for _, label in files_info]
    ax.bar(labels, results, yerr=np.array(errors).T, capsize=5, color=colors)
    ax.set_ylabel('Average Difference in Seconds')
    # ax.set_title('Average Time Difference From Original Gaps')

    # Annotating the min and max values on the bars
    for i, (min_val, max_val) in enumerate(min_max_values):
        bar = ax.patches[i]
        bar_height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, bar_height + errors[i][1], f"Max: {format_seconds(max_val)}", ha='center', va='bottom')
        ax.text(bar.get_x() + bar.get_width() / 2, bar_height - errors[i][0], f"Min: {format_seconds(min_val)}", ha='center', va='top')

    plt.savefig('plot_gap_duration_difference_plus1_min_max.png')

if __name__ == "__main__":
    main()
