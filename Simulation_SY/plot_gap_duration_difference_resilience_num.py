import re
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import os

def parse_duration(duration_str):
    h, m, s = map(float, duration_str.split(':'))
    return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

def get_original_duration(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'Total gap duration: (\d+:\d+:\d+\.\d+)', line)
            if match:
                return parse_duration(match.group(1))
    return None

def analyze_file(file_path, original_duration):
    durations = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'Total gap duration: (\d+:\d+:\d+\.\d+)', line)
            if match:
                duration = parse_duration(match.group(1))
                difference = abs(duration - original_duration)
                durations.append(difference.total_seconds())
    return durations

def format_seconds(seconds):
    hours = int(seconds // 3600)
    remaining_seconds = int(seconds % 3600)
    minutes = int(remaining_seconds // 60)
    remaining_seconds = int(remaining_seconds % 60)
    return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"

def main():
    directory = "Resilience"
    original_files = [
        'gap_duration_analysis_initial_20.txt',
        'gap_duration_analysis_initial_200.txt',
        'gap_duration_analysis_initial_500.txt',
        'gap_duration_analysis_initial_1000.txt',
        'gap_duration_analysis_initial_2000.txt'
    ]
    
    analyzed_files = [
        'gap_duration_analysis_resilience_20.txt',
        'gap_duration_analysis_resilience_200.txt',
        'gap_duration_analysis_resilience_500.txt',
        'gap_duration_analysis_resilience_1000.txt',
        'gap_duration_analysis_resilience_2000.txt'
    ]
    
    results = []
    errors = []
    avg_labels = []
    colors = ['blue', 'green', 'red', 'purple', 'gray']  # List of colors for each bar
    
    for original_file, analyzed_file in zip(original_files, analyzed_files):
        original_file_path = os.path.join(directory, original_file)
        analyzed_file_path = os.path.join(directory, analyzed_file)

        original_duration = get_original_duration(original_file_path)
        if not original_duration:
            print(f"Original duration not found for {original_file}.")
            continue

        durations = analyze_file(analyzed_file_path, original_duration)
        if durations:
            average_difference = np.mean(durations)
            std_deviation = np.std(durations)
            results.append(average_difference)
            errors.append(std_deviation)
            avg_labels.append(format_seconds(average_difference))
        else:
            results.append(0)  # Assuming zero difference if no durations found
            errors.append(0)
            avg_labels.append("00:00:00")

    # Setting larger font sizes
    plt.rcParams.update({'font.size': 14, 'axes.titlesize': 18, 'axes.labelsize': 16, 'xtick.labelsize': 14, 'ytick.labelsize': 14})

    # Plotting the results with error bars
    fig, ax = plt.subplots(figsize=(12, 8))  # Increase the figure size to 12x8 inches
    labels = [f"{base_name} Sats, {int(int(base_name)/2)} Denied" for base_name in ['20', '200', '500', '1000', '2000']]
    bars = ax.bar(labels, results, yerr=errors, capsize=5, color=colors)
    ax.set_ylabel('Avg. Difference (Seconds)')
    ax.set_title('Avg. Time Difference from Original Gaps')

    # Adding the average value on top of each bar
    for bar, label in zip(bars, avg_labels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, label, ha='center', va='bottom', fontsize=12)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()  # Adjust the layout to make room for the rotated labels
    plt.savefig('plot_gap_duration_difference_resilience_num.png', dpi=300)  # Save the figure with higher resolution
    # plt.show()

if __name__ == "__main__":
    main()
