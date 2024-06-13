import re
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import os
import plot_config

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
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02}:{remaining_seconds:02}"

def main():
    directory = "Resilience"
    original_file = 'gap_duration_analysis_initial_ratio_1000.txt'
    
    labels = [f"{i}_1" for i in range(1, 11)]
    analyzed_files = [f'gap_duration_analysis_resilience_1000_{label}.txt' for label in labels]
    
    results = []
    errors = []
    avg_labels = []
    num_labels = len(labels)  # Number of labels
    colors = plot_config.experiment_colors[:num_labels]
    hatches = plot_config.hatches[:num_labels]

    original_file_path = os.path.join(directory, original_file)
    original_duration = get_original_duration(original_file_path)
    if not original_duration:
        print(f"Original duration not found for {original_file}.")
        return

    for analyzed_file, label in zip(analyzed_files, labels):
        analyzed_file_path = os.path.join(directory, analyzed_file)

        durations = analyze_file(analyzed_file_path, original_duration)
        if durations:
            average_difference = np.mean(durations)
            std_deviation = np.std(durations)
            results.append(average_difference)
            errors.append(std_deviation)
            avg_labels.append(format_seconds(average_difference))
        else:
            results.append(0)  
            errors.append(0)
            avg_labels.append("00:00")

    new_labels = [f"{label.split('_')[0]}:1..:1" for label in labels]

    # Plotting the results with error bars
    fig, ax = plt.subplots(figsize=(12, 8))  # Increase the figure size to 12x8 inches
    bars = ax.bar(new_labels, results, yerr=errors, capsize=5, color=colors, hatch=hatches)
    ax.set_ylabel('Avg. Difference (Seconds)')
    ax.set_xlabel('Ratio Between Different Parties (Total: 1000 Satellites)')
    # ax.set_title('Avg. Time Difference from Original Gaps')

    # Adding the average value on top of each bar in MM:SS format
    for bar, label in zip(bars, avg_labels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * 0.85, height, label, ha='center', va='bottom', fontsize=12)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() 
    plt.savefig('plot_gap_duration_difference_resilience_ratio.png', dpi=300) 
    # plt.show()

if __name__ == "__main__":
    main()
