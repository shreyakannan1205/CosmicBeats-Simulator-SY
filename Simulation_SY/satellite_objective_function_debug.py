import pandas as pd
from datetime import datetime, timedelta
import sys

# Redirect stdout to a file
original_stdout = sys.stdout  # Save a reference to the original standard output
with open('objective_function_log.txt', 'w') as f:
    sys.stdout = f  # Change the standard output to the file we created.

    # Population data for each ground station
    population_data = {
        10001: 37115000,
        10002: 33807000,
        10003: 29868000,
        10004: 23936000,
        10005: 22807000,
        10006: 22623874,
        10007: 22624000,
        10008: 19034000,
        10009: 17649000,
        10010: 17032000,
        10011: 16536000,
        10012: 16047000,
        10013: 15618000,
        10014: 14942000,
        10015: 12712000,
        10016: 11658000,
        10017: 11436000,
        10018: 11362000,
        10019: 11277000,
        10020: 11234000,
        10021: 5316000
    }

    def parse_time(time_str):
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    def read_satellite_counts(node_id):
        counts_file = f'satellite_counts_node_{node_id}.txt'
        counts = {}
        with open(counts_file, 'r') as file:
            for line in file:
                parts = line.strip().split(' => count ')
                time = parse_time(parts[0])
                count = int(parts[1])
                counts[time] = count
        return counts

    def calculate_objective_function(passes_file, population_data):
        print(f"Processing file: {passes_file}")
        
        # Read passes data
        with open(passes_file, 'r') as file:
            lines = file.readlines()
        
        passes = []
        for line in lines:
            parts = line.strip().split('. ')
            node_id = int(parts[1].split(': ')[1])
            start_time = parse_time(parts[3].split(': ')[1])
            end_time = parse_time(parts[4].split(': ')[1])
            passes.append((node_id, start_time, end_time))
        
        # Calculate objective function
        total_score = 0
        
        for node_id, start_time, end_time in passes:
            population = population_data.get(node_id, 0)
            duration = int((end_time - start_time).total_seconds()) + 1
            
            # Read satellite count data for this node
            satellite_counts = read_satellite_counts(node_id)
            
            print(f"Calculating for nodeID: {node_id}, Population: {population}")
            print(f"Start Time: {start_time}, End Time: {end_time}, Duration: {duration} seconds")
            
            # Sum population / (number of satellites + 1) for each second in the duration
            for second in range(duration):
                current_time = start_time + timedelta(seconds=second)  # Generate each specific second
                if current_time in satellite_counts:  # Check if current_time is in satellite_counts
                    num_satellites = satellite_counts[current_time]
                    score = population / (num_satellites + 1)  # Include the satellite itself
                    total_score += score
                    print(f"  Time: {current_time}, Satellite Count: {num_satellites}, Score: {score}")
        
        print(f"Total Score for {passes_file}: {total_score}")
        return total_score

    # File paths for multiple passes files
    passes_files = [f'PlusOne_Phase_Objective/output_plus1_phase_{i}_sorted.txt' for i in range(1, 15)]

    # Calculate objective function for each passes file
    all_scores = []
    for passes_file in passes_files:
        score = calculate_objective_function(passes_file, population_data)
        all_scores.append((passes_file, score))

    # Print all objective function scores
    print("All Objective Function Scores:")
    for passes_file, score in all_scores:
        print(f"{passes_file}: {score}")

    # Reset stdout to the original standard output
    sys.stdout = original_stdout
