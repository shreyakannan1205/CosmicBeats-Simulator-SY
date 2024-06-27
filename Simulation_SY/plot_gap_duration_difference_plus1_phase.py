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
    directory = "PlusOne_Phase"
    ground_stations = get_ground_stations()

    satellite_numbers = []
    weighted_avg_coverage_time_diff = []

    max_satellites = 0
    for city, population in ground_stations:
        filename = f"output_plus1_phase_gap_duration_analysis_{city}.txt"
        full_path = os.path.join(directory, filename)
        with open(full_path, 'r') as file:
            lines = file.readlines()
            if len(lines) - 1 > max_satellites:
                max_satellites = len(lines) - 1 

    for satellite_num in range(max_satellites):
        total_durations = []
        for city, population in ground_stations:
            filename = f"output_plus1_phase_gap_duration_analysis_{city}.txt"
            folder_path = directory
            durations = analyze_file_shorter(folder_path, filename, population)
            if len(durations) > satellite_num:
                total_durations.append(durations[satellite_num])

        if total_durations:
            population_weighted_avg_diff = sum(total_durations) / (sum(population for _, population in ground_stations) * len(total_durations) / len(ground_stations))
            satellite_numbers.append((satellite_num + 1) * 120.284924)  # Multiply by 120.284924 to get the distance
            weighted_avg_coverage_time_diff.append(population_weighted_avg_diff)
            print(f"Satellite {satellite_num + 1}: Avg={population_weighted_avg_diff}")
        else:
            print(f"No durations found for satellite {satellite_num + 1}")

    plt.figure(figsize=(10, 6))
    plt.plot(satellite_numbers, weighted_avg_coverage_time_diff, marker='o', linestyle='-')
    plt.xlabel('Distance from Original Satellite (km)')
    plt.ylabel('Difference in Coverage \n (min)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.savefig("plot_gap_duration_difference_plus1_phase.png")
    print("Plot saved as 'plot_gap_duration_difference_plus1_phase.png'")

if __name__ == "__main__":
    main()
