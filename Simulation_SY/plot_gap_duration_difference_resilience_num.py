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
    colors = plot_config.experiment_colors[:len(original_files)]
    hatches = plot_config.hatches[:len(original_files)]

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
            results.append(0)  
            errors.append(0)
            avg_labels.append("00:00:00")

    fig, ax = plt.subplots() 
    labels = [f"{base_name}" for base_name in ['20', '200', '500', '1000', '2000']]
    bars = ax.bar(labels, results, yerr=errors, capsize=5, color=colors, hatch=hatches)
    ax.set_xlabel('Total Number of Satellites')
    ax.set_ylabel('Avg. Difference (Seconds)')
    # ax.set_title('Avg. Time Difference from Original Gaps')

    for bar, label in zip(bars, avg_labels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * 0.85, height, label, ha='center', va='bottom', fontsize=plot_config.annotation_fontsize)

    plt.xticks()
    plt.tight_layout() 
    plt.savefig('plot_gap_duration_difference_resilience_num.png', dpi=300)  
    # plt.show()

if __name__ == "__main__":
    main()
