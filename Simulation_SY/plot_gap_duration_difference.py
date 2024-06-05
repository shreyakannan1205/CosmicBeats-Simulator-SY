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

def main():
    files_info = [
        ('gap_duration_analysis_plus1_1.txt', "one plus one"),
        ('gap_duration_analysis_plus1_100.txt', "hundred plus one"),
        ('gap_duration_analysis_plus1_500.txt', "fivehundred plus one")
    ]
    results = []
    errors = []
    colors = ['blue', 'green', 'red']  # List of colors for each bar

    for filename, label in files_info:
        durations = analyze_file(filename)
        if durations:
            average_difference = np.mean(durations)
            std_deviation = np.std(durations)
            results.append(average_difference)
            errors.append(std_deviation)
        else:
            results.append(0)  # Assuming zero difference if no durations found
            errors.append(0)

    # Plotting the results with error bars
    fig, ax = plt.subplots()
    labels = [label for _, label in files_info]
    ax.bar(labels, results, yerr=errors, capsize=5, color=colors)
    ax.set_ylabel('Average Difference in Seconds')
    ax.set_title('Average Time Difference From Original Gaps')
    plt.savefig('plot_gap_duration_difference.png')

if __name__ == "__main__":
    main()
