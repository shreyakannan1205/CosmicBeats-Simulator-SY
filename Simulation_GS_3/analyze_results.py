import os 
import csv
import json
#distances = [10,20,50]
distances = [10,20,50]
numsat = 1000
#stored as [d: {"random": X, X'}, {"max": X,X'}]

results = {}

base_path = "/home/shreya28/CosmicBeats-Simulator-SY/Simulation_GS_3/results/"

for d in distances:
    file_max = f"results_{numsat}_{d}_max.csv"
    file_random = f"results_{numsat}_{d}_random.csv"
    files = [file_max, file_random]
    results[d] = {}

    for file in files:
        cat = file.split("_")[3][:-4]
        true_count = 0
        false_count = 0
        with open(base_path + file, 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if "True" in row[1]:
                    true_count += 1
                else:
                    false_count += 1
        
        results[d][cat] = [true_count, false_count]
print(results)
with open("basic_results.json", 'w') as f:
    json.dump(results,f)




