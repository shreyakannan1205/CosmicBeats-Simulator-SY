import pandas as pd

# Load the data from the text file
file_path = 'output_5000_random_10km.txt'
output_file = 'results_5000.csv'  # File to save the results
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
def analyze_snr(df):
    results = []
    grouped = df.groupby('timestamp')
    
    for timestamp, group in grouped:
        gs_10001 = group[group['ground_station'] == 10001]
        gs_10002 = group[group['ground_station'] == 10002]
        
        if not gs_10001.empty and not gs_10002.empty:
            # Find the satellite with the largest SNR for both ground stations
            max_snr_10001 = gs_10001.loc[gs_10001['snr'].idxmax()]['satellite']
            max_snr_10002 = gs_10002.loc[gs_10002['snr'].idxmax()]['satellite']
            
            if max_snr_10001 == max_snr_10002:
                results.append((timestamp, True, max_snr_10001))
            else:
                results.append((timestamp, False, (max_snr_10001, max_snr_10002)))
        else:
            # If there's only one satellite, assume it's the largest for both stations
            unique_satellite = group['satellite'].iloc[0]
            results.append((timestamp, True, unique_satellite))
    
    return pd.DataFrame(results, columns=['timestamp', 'same_satellite', 'satellite'])

# Analyze the SNR data
results_df = analyze_snr(df)

# Save the results to a CSV file
results_df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
