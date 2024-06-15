import re
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import os
import plot_config

def parse_duration(duration_str):
    if "days" in duration_str:
        days, time_str = duration_str.split(", ")
        days = int(days.split()[0])
        h, m, s = map(float, time_str.split(':'))
        # print(f"Parsing duration: {days} days, {h}:{m}:{s}")
        return timedelta(days=days, hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))
    else:
        h, m, s = map(float, duration_str.split(':'))
        # print(f"Parsing duration: {h}:{m}:{s}")
        return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

def analyze_file(folder_path, filename, population):
    durations = []
    original_duration = None

    full_path = os.path.join(folder_path, filename)
    # print(f"Analyzing file: {full_path}")
    with open(full_path, 'r') as file:
        first_line = next(file)
        match = re.search(r'Total gap duration: (\d+ days, \d+:\d+:\d+\.\d+|\d+:\d+:\d+\.\d+)', first_line)
        if match:
            original_duration = parse_duration(match.group(1))
            print(f"Original duration: {original_duration}")

        if not original_duration:
            print(f"No original duration found in file: {filename}")
            return durations

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
                # print(f"Duration: {duration}, Difference: {difference}, Weighted Difference: {weighted_difference}")

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
        # ("moscow", 12506468),
        ("sydney", 5312163),
        ("seoul", 9733509),
        ("paris", 2161000)
    ]

    files_info = [
        ('1', "1 + 1"),
        ('100', "100 + 1"),
        ('500', "500 + 1")
    ]

    results = []
    errors = []
    min_max_values = []
    colors = plot_config.experiment_colors[:len(files_info)]
    hatches = plot_config.hatches[:len(files_info)]
    annotation_fontsize = plot_config.annotation_fontsize

    total_population = sum(population for _, population in ground_stations)
    num_cities = len(ground_stations)

    for file_prefix, label in files_info:
        # print(f"Processing file prefix: {file_prefix}, label: {label}")
        total_durations = []
        for city, population in ground_stations:
            filename = f"gap_duration_analysis_plus1_{file_prefix}_{city}.txt"
            folder_path = "PlusOne"
            durations = analyze_file(folder_path, filename, population)
            total_durations.extend(durations)
            #  print(f"Durations for {city}: {durations}")

        if total_durations:
            num_durations = len(total_durations)
            population_weighted_avg_diff = sum(total_durations) / (total_population * num_durations / num_cities)
            min_difference = np.min(total_durations)
            max_difference = np.max(total_durations)
            results.append(population_weighted_avg_diff)
            errors.append([abs(population_weighted_avg_diff - min_difference / (total_population / num_cities)), 
                           abs(max_difference / (total_population / num_cities) - population_weighted_avg_diff)])
            min_max_values.append((min_difference, max_difference))
            print(f"Results for {label}: Avg={population_weighted_avg_diff}, Min={min_difference}, Max={max_difference}")
        else:
            results.append(0)
            errors.append([0, 0])
            min_max_values.append((0, 0))
            print(f"No durations found for file prefix: {file_prefix}")

    fig, ax = plt.subplots(figsize = (15,6))
    labels = [label for _, label in files_info]
    ax.bar(labels, results, yerr=np.array(errors).T, capsize=5, color=colors, hatch=hatches)
    ax.set_ylabel('Population-Weighted \n Average Coverage Difference \n (Seconds)')
    ax.set_xlabel('Base Number of Satellites (1, 100, 500)')
    # ax.set_title('Average Time Difference From Original Gaps')

    for i, (min_val, max_val) in enumerate(min_max_values):
        bar = ax.patches[i]
        bar_height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, bar_height + errors[i][1], f"Max: {format_seconds(max_val / (total_population / num_cities))}", ha='center', va='bottom', fontsize=annotation_fontsize)
        # ax.text(bar.get_x() + bar.get_width() / 2, bar_height - errors[i][0], f"Min: {format_seconds(min_val / total_population)}", ha='center', va='top', fontsize=annotation_fontsize)

    plt.savefig('plot_gap_duration_difference_plus1_min_max_cities.png', dpi=300)
    print("Plot saved as 'plot_gap_duration_difference_plus1_min_max_cities.png'")

if __name__ == "__main__":
    main()
