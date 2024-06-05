import re
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import os

def parse_duration(duration_str):
    h, m, s = map(float, duration_str.split(':'))
    return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

def get_original_duration():
    original_file = 'gap_duration_analysis_plus1_original.txt'
    folder_path = "Ablation"
    full_path = os.path.join(folder_path, original_file)
    
    with open(full_path, 'r') as file:
        for line in file:
            match = re.search(r'Total gap duration: (\d+:\d+:\d+\.\d+)', line)
            if match:
                return parse_duration(match.group(1))
    return None

def analyze_file(filename, original_duration):
    durations = []
    folder_path = "Ablation"  # Define the folder where files are stored

    full_path = os.path.join(folder_path, filename)  # Generate the full path to the file
    with open(full_path, 'r') as file:
        for line in file:
            match = re.search(r'Total gap duration: (\d+:\d+:\d+\.\d+)', line)
            if match:
                duration = parse_duration(match.group(1))
                difference = abs(duration - original_duration)
                durations.append(difference.total_seconds())

    return durations

def format_seconds(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02}:{remaining_seconds:02}"

def main():
    original_duration = get_original_duration()
    if not original_duration:
        print("Original duration not found.")
        return

    files_info = [
        ('gap_duration_analysis_plus1_diffheight.txt', "Different Height Sat"),
        ('gap_duration_analysis_plus1_diffinclination.txt', "Different Inclination Sat"),
        ('gap_duration_analysis_plus1_diffphase.txt', "Different Phase Sat")
    ]
    results = []
    errors = []
    avg_labels = []
    colors = ['blue', 'green', 'red']  # List of colors for each bar

    for filename, label in files_info:
        durations = analyze_file(filename, original_duration)
        if durations:
            average_difference = np.mean(durations)
            std_deviation = np.std(durations)
            results.append(average_difference)
            errors.append(std_deviation)
            avg_labels.append(format_seconds(average_difference))
        else:
            results.append(0)  # Assuming zero difference if no durations found
            errors.append(0)
            avg_labels.append("00:00")

    # Plotting the results with error bars
    fig, ax = plt.subplots()
    labels = [label for _, label in files_info]
    bars = ax.bar(labels, results, yerr=errors, capsize=5, color=colors)
    ax.set_ylabel('Average Difference in Seconds')
    ax.set_title('Average Time Difference From Original Gaps')

    # Adding the average value on top of each bar
    for bar, label in zip(bars, avg_labels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, label, ha='center', va='bottom')

    plt.savefig('plot_gap_duration_difference_ablation.png')

if __name__ == "__main__":
    main()
