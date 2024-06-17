import matplotlib.pyplot as plt
import sys
import plot_config

# Read the summary file
summary_file_path = 'NumSat/summary_file.txt'

number_of_sats = []
useless_ratios = []

with open(summary_file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        # print(f"Processing line: {line.strip()}")
        parts = line.strip().split(': Useless timestamp ratio: ')
        if len(parts) == 2:
            try:
                file_name_part = parts[0].strip().split('_')
                # print(f"Parsed file_name_part: {file_name_part}")
                file_size = int(file_name_part[1])
                useless_ratio = float(parts[1])
                number_of_sats.append(file_size)
                useless_ratios.append(useless_ratio)
            except (IndexError, ValueError) as e:
                print(f"Error parsing line: {line.strip()}")
                print(f"Exception: {e}")

# Ensure there is data to plot
if not number_of_sats or not useless_ratios:
    print("No data to plot. Please check the summary file for correct format.")
    sys.exit(1)

# Sort the data by file size
sorted_data = sorted(zip(number_of_sats, useless_ratios))
number_of_sats, useless_ratios = zip(*sorted_data)

# Plot the data
plt.figure()
plt.plot(number_of_sats, useless_ratios, marker='o')
# plt.title('Useless Timestamp Ratio vs. File Size')
plt.xlabel('Number of Satellites')
plt.ylabel('Useless Pass (Timestamp) Ratio')
plt.grid(True)
# plt.show()
plt.savefig('plot_numsat_useless_timestamps.png')