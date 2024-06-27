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

def analyze_file_longer_ratio(folder_path, filename, original_duration, population):
    durations = []
    full_path = os.path.join(folder_path, filename)

    with open(full_path, 'r') as file:
        for line in file:
            match = re.search(r'Total gap duration: ((\d+ days, \d+:\d+:\d+\.\d+|\d+ day, \d+:\d+:\d+\.\d+|\d+:\d+:\d+\.\d+|0:00:00))', line)
            if match:
                duration = parse_duration(match.group(1))
                if duration < original_duration:
                    print(f"Error: Found a duration shorter than the original duration in file {filename}: {duration}")
                    continue
                difference = duration - original_duration
                weighted_difference = difference.total_seconds() * population / 60  # Convert to minutes
                durations.append(weighted_difference)

    return durations

def format_minutes(minutes):
    hours = int(minutes // 60)
    minutes = int(minutes % 60)
    return f"{hours} hours, {minutes} minutes" if hours > 0 else f"{minutes} minutes"

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
    directory = "Robustness_Ratio"
    
    labels = [f"{i}_1" for i in range(1, 11)]
    ground_stations = get_ground_stations()
    
    results = []
    errors = []
    avg_labels = []
    num_labels = len(labels)
    colors = plot_config.experiment_colors[:num_labels]
    hatches = plot_config.hatches[:num_labels]
    
    total_population = sum(population for _, population in ground_stations)

    for label in labels:
        total_durations = []
        for city, population in ground_stations:
            original_filename = f"output_robustness_ratio_1000_gap_duration_analysis_{city}.txt"

            original_duration = None
            original_path = os.path.join(directory, original_filename)
            with open(original_path, 'r') as file:
                first_line = next(file)
                match = re.search(r'Total gap duration: ((\d+ days, \d+:\d+:\d+\.\d+|\d+ day, \d+:\d+:\d+\.\d+|\d+:\d+:\d+\.\d+|0:00:00))', first_line)
                if match:
                    original_duration = parse_duration(match.group(1))
                    print(f"Original duration for city {city}: {original_duration}")

            if original_duration is None:
                print(f"No original duration found in file: {original_filename}")
                continue

            filename = f"output_robustness_ratio_1000_{label}_gap_duration_analysis_{city}.txt"
            durations = analyze_file_longer_ratio(directory, filename, original_duration, population)
            total_durations.extend(durations)

        if total_durations:
            num_durations = len(total_durations)
            population_weighted_avg_diff = sum(total_durations) / (total_population * num_durations / len(ground_stations))
            std_deviation = np.std(total_durations) / total_population
            results.append(population_weighted_avg_diff)
            errors.append(std_deviation)
            avg_labels.append(format_minutes(population_weighted_avg_diff))
        else:
            results.append(0)
            errors.append(0)
            avg_labels.append("0 minutes")
            print(f"No durations found for satellite ratio {label}")

    new_labels = [f"{label.split('_')[0]}:1..:1" for label in labels]

    fig, ax = plt.subplots(figsize = (10,7))
    bars = ax.bar(new_labels, results, yerr=errors, capsize=5, color=colors, hatch=hatches)
    ax.set_ylabel('Difference in Coverage \n (min)')
    ax.set_xlabel('Ratio Between Different Parties')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.savefig('plot_gap_duration_difference_robustness_ratio.png', dpi=300)
    print("Plot saved as 'plot_gap_duration_difference_robustness_ratio.png'")

if __name__ == "__main__":
    main()
