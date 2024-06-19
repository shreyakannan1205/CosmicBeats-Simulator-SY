import re
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import os
import plot_config

def parse_duration(duration_str):
    if duration_str == "0:00:00":
        return timedelta(seconds=0)
    if "day" in duration_str:
        days, time_str = duration_str.split(", ")
        days = int(days.split()[0])
        h, m, s = map(float, time_str.split(':'))
        return timedelta(days=days, hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))
    else:
        h, m, s = map(float, duration_str.split(':'))
        return timedelta(hours=h, minutes=m, seconds=int(s), microseconds=int((s - int(s)) * 1e6))

def analyze_file_shorter(folder_path, filename, population):
    durations = []
    original_duration = None

    full_path = os.path.join(folder_path, filename)
    with open(full_path, 'r') as file:
        first_line = next(file)
        match = re.search(r'Total gap duration: (\d+ days, \d+:\d+:\d+\.\d+|\d+ day, \d+:\d+:\d+\.\d+|\d+:\d+:\d+\.\d+|0:00:00)', first_line)
        if match:
            original_duration = parse_duration(match.group(1))
            print(f"Original duration: {original_duration}")

        if original_duration is None:
            print(f"No original duration found in file: {filename}")
            return durations

        for line in file:
            match = re.search(r'Total gap duration: (\d+ days, \d+:\d+:\d+\.\d+|\d+ day, \d+:\d+:\d+\.\d+|\d+:\d+:\d+\.\d+|0:00:00)', line)
            if match:
                duration = parse_duration(match.group(1))
                if duration > original_duration:
                    print(f"Error: Found a duration longer than the original duration in file {filename}: {duration}")
                    continue
                difference = original_duration - duration
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

def get_ground_stations():
    return [
        ("10001", 37115000), # Tokyo (Japan)
        ("10002", 33807000), # Delhi (India)
        ("10003", 29868000), # Shanghai (China)
        ("10004", 23936000), # Dhaka (Bangladesh)
        ("10005", 22807000), # Sao Paulo (Brazil)
        ("10006", 22623874), # Cairo (Egypt)
        ("10007", 22624000), # Mexico City (Mexico)
        ("10008", 19034000), # New York (USA)
        ("10009", 17649000), # Karachi (Pakistan)
        ("10010", 17032000), # Kinshasa (DR Congo)
        ("10011", 16536000), # Lagos (Nigeria)
        ("10012", 16047000), # Istanbul (Turkey)
        ("10013", 15618000), # Buenos Aires (Argentina)
        ("10014", 14942000), # Manila (Philippines)
        ("10015", 12712000), # Moscow (Russia)
        ("10016", 11658000), # Bogota (Columbia)
        ("10017", 11436000), # Jakarta (Indonesia)
        ("10018", 11362000), # Lima (Peru)
        ("10019", 11277000), # Paris (France)
        ("10020", 11234000), # Bangkok (Thailand)
        ("10021", 5316000), # Melbourne (Australia)
    ]

def main():
    ground_stations = get_ground_stations()

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
        total_durations = []
        for city, population in ground_stations:
            filename = f"output_plus1_{file_prefix}_gap_duration_analysis_{city}.txt"
            folder_path = "PlusOne"
            durations = analyze_file_shorter(folder_path, filename, population)
            total_durations.extend(durations)

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
