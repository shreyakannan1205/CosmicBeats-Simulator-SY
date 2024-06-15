import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import plot_config

# Directory containing the gap duration files
directory = "PlusOne_Phase"

# List of cities and their corresponding files and populations
cities_info = [
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

# Initialize a dictionary to store data
data = {f"Imaginary_{i}": [] for i in range(1, 90)}

# Helper function to convert time string to timedelta
def str_to_timedelta(time_str):
    if "days" in time_str:
        days, time_str = time_str.split(", ")
        days = int(days.split(" ")[0])
        h, m, s = map(float, time_str.split(':'))
        return timedelta(days=days, hours=h, minutes=m, seconds=s)
    else:
        h, m, s = map(float, time_str.split(':'))
        return timedelta(hours=h, minutes=m, seconds=s)

# Function to get the initial gap duration
def get_initial_gap_duration(city):
    file_path = os.path.join(directory, f"gap_duration_analysis_initial_plus1_{city}.txt")
    if not os.path.exists(file_path):
        print(f"Initial file not found: {file_path}")
        return None
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if line.startswith("Total gap duration:"):
            total_gap_duration_str = line.split(": ")[1].strip()
            return str_to_timedelta(total_gap_duration_str)
    
    print(f"Total gap duration not found in initial file for {city}")
    return None

# Read distances from distance_fixed.txt
distance_file_path = os.path.join(directory, "distance_fixed.txt")
distances = []
with open(distance_file_path, 'r') as file:
    for line in file:
        distances.append(float(line.strip()))

# Process each city's file
for city, population in cities_info:
    initial_gap_duration = get_initial_gap_duration(city)
    if initial_gap_duration is None:
        continue
    
    file_path = os.path.join(directory, f"gap_duration_analysis_plus1_{city}.txt")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for i in range(0, len(lines), 4):
        if i + 3 >= len(lines):
            print(f"Unexpected file format in {file_path}, line {i+3} is missing")
            continue
        
        satellite = lines[i].strip()
        if lines[i+3].startswith("Total gap duration:"):
            total_gap_duration_str = lines[i+3].split(": ")[1].strip()
            total_gap_duration = str_to_timedelta(total_gap_duration_str)
            coverage_time_diff = initial_gap_duration - total_gap_duration
            
            if satellite in data:
                # Multiply coverage time difference by city population
                weighted_coverage_time_diff = coverage_time_diff.total_seconds() * population
                data[satellite].append(weighted_coverage_time_diff)

# Calculate the total population
total_population = sum(population for city, population in cities_info)

# Calculate the population-weighted average coverage time difference for each satellite
weighted_avg_coverage_time_diff = {sat: sum(times) / total_population for sat, times in data.items()}

# Use distances as x-axis values
x_values = [distances[int(sat.split("_")[1]) - 1] for sat in weighted_avg_coverage_time_diff.keys()]

# Plotting the population-weighted average coverage time difference for each satellite
plt.figure(figsize=(15, 6))
plt.plot(x_values, list(weighted_avg_coverage_time_diff.values()), marker='o', linestyle='-', color='skyblue')
plt.xlabel('Distance from Satellite 0 (km)')
plt.ylabel('Population-Weighted \n Average Coverage Time Difference \n (seconds)')
plt.grid(True)

# Save the plot
plt.savefig("plot_gap_duration_difference_plus1_90_distance.png")
