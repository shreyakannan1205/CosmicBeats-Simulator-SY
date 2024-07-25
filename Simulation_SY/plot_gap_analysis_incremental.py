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

def analyze_file_7days(folder_path, filename, population):
    durations = []
    original_duration = timedelta(days=7)  # 7 days

    full_path = os.path.join(folder_path, filename)
    with open(full_path, 'r') as file:
        for line in file:
            match = re.search(r'Total gap duration: (\d+ days, \d+:\d+:\d+\.\d+|\d+ day, \d+:\d+:\d+\.\d+|\d+:\d+:\d+\.\d+|0:00:00)', line)
            if match:
                duration = parse_duration(match.group(1))
                if duration > original_duration:
                    print(f"Error: Found a duration longer than the original duration in file {filename}: {duration}")
                    continue
                difference = original_duration - duration
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
    ground_stations = get_ground_stations()

    files_info = [
        ('output_incremental_5_all', "All"),
        ('output_incremental_5_incremental', "Incremental")
    ]

    results = []
    errors = []
    colors = plot_config.experiment_colors[:len(files_info)]
    hatches = plot_config.hatches[:len(files_info)]
    annotation_fontsize = plot_config.annotation_fontsize

    total_population = sum(population for _, population in ground_stations)
    num_cities = len(ground_stations)

    for file_prefix, label in files_info:
        total_durations = []
        city_durations = {}
        for city, population in ground_stations:
            filename = f"{file_prefix}_gap_duration_analysis_{city}.txt"
            folder_path = "Incremental"
            durations = analyze_file_7days(folder_path, filename, population)
            total_durations.extend(durations)
            city_durations[city] = durations

        if total_durations:
            num_durations = len(total_durations)
            population_weighted_avg_diff = sum(total_durations) / (total_population * num_durations / num_cities)
            std_deviation = np.std(total_durations) / total_population
            results.append(population_weighted_avg_diff)
            errors.append(std_deviation)
            print(f"Results for {label}: Avg={population_weighted_avg_diff}, Std Dev={std_deviation}")
            
        else:
            results.append(0)
            errors.append(0)
            print(f"No durations found for file prefix: {file_prefix}")

    fig, ax = plt.subplots()
    labels = [label for _, label in files_info]
    bars = ax.bar(labels, results, yerr=errors, capsize=5, color=colors, hatch=hatches, width=0.5)
    ax.set_xlabel('Type of Satellite Constellation')
    ax.set_ylabel('Coverage \n (min)')
    # ax.set_title('Average Time Difference From Original Gaps')

    plt.tight_layout()
    plt.savefig('plot_gap_analysis_incremental.png', dpi=300)
    print("Plot saved as 'plot_gap_analysis_incremental.png'")

if __name__ == "__main__":
    main()
