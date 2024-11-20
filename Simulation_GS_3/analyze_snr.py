import pandas as pd
import os

# Load the data from the text file

d = 10
numsat = 1000

file_path = os.getcwd() +"/" + os.path.join("outputs",f'output_{numsat}_{d}.txt')
output_file_random =  os.getcwd() +"/" + os.path.join("results",f'results_{numsat}_{d}_random.csv') # File to save the results
output_file_max =   os.getcwd() +"/" +os.path.join("results",f'results_{numsat}_{d}_max.csv')

columns = ['snr', 'ground_station', 'satellite', 'date', 'time', 'distance']
data = []

# Parse the file
with open(file_path, 'r') as file:
    for line in file:
        parts = line.split()
        # Ensure the line has the expected number of elements
        if len(parts) == 6:
            try:
                snr = float(parts[0])
                ground_station = int(parts[1])
                satellite = int(parts[2])
                date = parts[3]
                time = parts[4]
                distance = float(parts[5])
                data.append([snr, ground_station, satellite, date, time, distance])
            except ValueError:
                # Skip the line if conversion fails without printing anything
                continue
        else:
            # Skip the line if it doesn't have the correct number of elements without printing anything
            continue

# Convert to DataFrame
df = pd.DataFrame(data, columns=columns)

# Combine date and time into a single timestamp column
df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Drop the separate date and time columns
df = df.drop(columns=['date', 'time'])

# Function to check if the satellite with the largest SNR is the same for both ground stations
def analyze_max_snr(df):
    results = []
    grouped = df.groupby('timestamp')
    
    for timestamp, group in grouped:
        gs_10001 = group[group['ground_station'] == 10001]
        gs_10002 = group[group['ground_station'] == 10002]
        gs_10003 = group[group['ground_station'] == 10003]

        if not gs_10001.empty and not gs_10002.empty and not gs_10003.empty:
            # Find the satellite with the largest SNR for both ground stations
            max_snr_10001 = gs_10001.loc[gs_10001['snr'].idxmax()]['satellite']
            max_snr_10002 = gs_10002.loc[gs_10002['snr'].idxmax()]['satellite']
            max_snr_10003 = gs_10003.loc[gs_10003['snr'].idxmax()]['satellite']

            if max_snr_10001 == max_snr_10002 and max_snr_10002 == max_snr_10003:
                results.append((timestamp, True, max_snr_10001))
            else:
                results.append((timestamp, False, (max_snr_10001, max_snr_10002, max_snr_10003)))
        else:
            # If there's only one satellite, assume it's the largest for both stations
            unique_satellite = group['satellite'].iloc[0]
            results.append((timestamp, True, unique_satellite))
    
    return pd.DataFrame(results, columns=['timestamp', 'same_satellite', 'satellite'])

def analyze_random_snr(df):
    results = []
    grouped = df.groupby('timestamp')
    
    for timestamp, group in grouped:
        gs_10001 = group[group['ground_station'] == 10001]
        gs_10002 = group[group['ground_station'] == 10002]
        gs_10003 = group[group['ground_station'] == 10003]

        if not gs_10001.empty and not gs_10002.empty and not gs_10003.empty:
            # Find the satellite with the largest SNR for both ground stations

            sat_10001 = gs_10001.sample(n=1)["satellite"].iloc[0]
            sat_10002 = gs_10002.sample(n=1)["satellite"].iloc[0]
            sat_10003 = gs_10003.sample(n=1)["satellite"].iloc[0]

            if sat_10001 == sat_10002 and sat_10002 == sat_10003:
                results.append((timestamp, True, sat_10001))
            else:
                results.append((timestamp, False, (sat_10001, sat_10002, sat_10003)))
        else:

            unique_satellite = group['satellite'].iloc[0]
            results.append((timestamp, "One satellite case/True", unique_satellite))
    
    return pd.DataFrame(results, columns=['timestamp', 'same_satellite', 'satellite'])

# Analyze the SNR data
# Save the results to a CSV file
results_df_max = analyze_max_snr(df)
results_df_max.to_csv(output_file_max, index=False)
print(f"Results max saved to {output_file_max}")

# Save the results to a CSV file
results_df_random = analyze_random_snr(df)
results_df_random.to_csv(output_file_random, index=False)
print(f"Results random saved to {output_file_random}")
