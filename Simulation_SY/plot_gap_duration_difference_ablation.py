import re
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import os
import plot_config

def parse_duration(duration_str):
    if "days" in duration_str:
        days, time_str = duration_str.split(", ")
        days = int(days.split(" ")[0])
        h, m, s = map(float, time_str.split(':'))
        return timedelta(days=days, hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))
    else:
        h, m, s = map(float, duration_str.split(':'))
        return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

def get_original_duration(city, config):
    original_file = f'gap_duration_analysis_initial_plus1_{config}_{city}.txt'
    folder_path = "Ablation"
    full_path = os.path.join(folder_path, original_file)

    with open(full_path, 'r') as file:
        for line in file:
            match = re.search(r'Total gap duration: (\d+ days, \d+:\d+:\d+\.\d+|\d+:\d+:\d+\.\d+)', line)
            if match:
                return parse_duration(match.group(1))
    return None

def analyze_file(folder_path, filename, original_duration, population):
    durations = []

    full_path = os.path.join(folder_path, filename)
    with open(full_path, 'r') as file:
        for line in file:
            match = re.search(r'Total gap duration: (\d+ days, \d+:\d+:\d+\.\d+|\d+:\d+:\d+\.\d+)', line)
            if match:
                duration = parse_duration(match.group(1))
                if duration > original_duration:
                    print(f"Error: Found a duration longer than the original duration in file {filename}: {duration}")
                    continue
                difference = (original_duration - duration)
                weighted_difference = difference.total_seconds() * population
                durations.append(weighted_difference)

    return durations

def format_seconds(seconds):
    days = int(seconds // (24 * 3600))
    seconds %= (24 * 3600)
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    if days > 0:
        return f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:02}"

def main():
    ground_stations = [
        ("taipei", 2646204),
        ("ny", 8336817),
        ("saopaulo", 12325232),
        ("mumbai", 20667656),
        ("la", 3898747),
        ("lagos", 14862000),
        ("moscow", 12506468),
        ("sydney", 5312163),
        ("seoul", 9733509),
        ("paris", 2161000)
    ]

    files_info = [
        ('diffheight', "Different Height"),
        ('diffinclination', "Different Inclination"),
        ('diffphase', "Different Phase")
    ]

    results = []
    avg_labels = []
    colors = plot_config.experiment_colors[:len(files_info)]
    hatches = plot_config.hatches[:len(files_info)]
    total_population = sum(population for _, population in ground_stations)
    num_cities = len(ground_stations)

    for file_prefix, label in files_info:
        total_durations = []
        for city, population in ground_stations:
            original_duration = get_original_duration(city, file_prefix)
            if not original_duration:
                print(f"Original duration not found for {city} with config {file_prefix}.")
                continue

            filename = f"gap_duration_analysis_plus1_{file_prefix}_{city}.txt"
            durations = analyze_file("Ablation", filename, original_duration, population)
            total_durations.extend(durations)

        if total_durations:
            num_durations = len(total_durations)
            population_weighted_avg_diff = sum(total_durations) / (total_population * num_durations / num_cities)
            results.append(population_weighted_avg_diff)
            avg_labels.append(format_seconds(population_weighted_avg_diff))
        else:
            results.append(0)
            avg_labels.append("00:00")

    fig, ax = plt.subplots(figsize=(15,6))
    labels = [label for _, label in files_info]
    bars = ax.bar(labels, results, color=colors, hatch=hatches)
    ax.set_xlabel('Type of Satellite Added')
    ax.set_ylabel('Population-Weighted \n Average Coverage Difference \n (Seconds)')
    # ax.set_title('Average Time Difference From Original Gaps')

    for bar, label in zip(bars, avg_labels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * 0.5, height, label, ha='center', va='bottom', fontsize=plot_config.annotation_fontsize)

    plt.savefig('plot_gap_duration_difference_ablation.png', dpi=300)
    print("Plot saved as 'plot_gap_duration_difference_ablation.png'")

if __name__ == "__main__":
    main()
