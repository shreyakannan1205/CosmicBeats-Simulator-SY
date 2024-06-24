import argparse
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_passes(file_path):
    passes_by_node = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Pass."):
                parts = line.split(". ")
                node_id = int(parts[1].split(": ")[1])
                start_time_str = parts[3].split(": ")[1].strip()
                end_time_str = parts[4].split(": ")[1].strip()
                start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
                end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
                start_time_unix = start_time.timestamp()
                end_time_unix = end_time.timestamp()
                passes_by_node[node_id].append((start_time_unix, end_time_unix))
    return passes_by_node

def count_satellites_over_station(passes, target_time):
    target_time_unix = target_time.timestamp()
    count = 0
    for start_time_unix, end_time_unix in passes:
        if start_time_unix <= target_time_unix <= end_time_unix:
            count += 1
    return count

def save_counts_to_file(passes_by_node, target_time):
    for node_id, passes in passes_by_node.items():
        output_file_path = f'satellite_counts_node_{node_id}.txt'
        with open(output_file_path, 'w') as output_file:
            for i in range(604800):  # 24 hours * 3600 seconds
                current_time = target_time + datetime.timedelta(seconds=i)
                count = count_satellites_over_station(passes, current_time)
                output_file.write(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} => count {count}\n")

def plot_counts(node_id, file_path):
    times = []
    counts = []
    with open(file_path, 'r') as file:
        for line in file:
            if '=>' in line:
                parts = line.split(' => count ')
                times.append(datetime.datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S'))
                counts.append(int(parts[1].strip()))

    plt.figure(figsize=(12, 6))
    plt.plot(times, counts, label=f'NodeID {node_id} Satellite Count')
    plt.xlabel('Time')
    plt.ylabel('Satellite Count')
    plt.title(f'Satellite Count Over Time for NodeID {node_id}', fontsize=20)
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'satellite_counts_node_{node_id}.png')
    
def main():
    parser = argparse.ArgumentParser(description='Count satellites over a ground station at a specific time.')
    parser.add_argument('file_path', type=str, help='Path to the input file')
    parser.add_argument('target_time', type=str, help='Target time in the format YYYY-MM-DD HH:MM:SS')
    parser.add_argument('--plot_node_id', type=int, help='NodeID to plot', required=True)

    args = parser.parse_args()

    # Convert the target time string to a datetime object
    target_time = datetime.datetime.strptime(args.target_time, '%Y-%m-%d %H:%M:%S')

    # Parse passes from the file
    passes_by_node = parse_passes(args.file_path)

    # Save the satellite counts to the output files
    save_counts_to_file(passes_by_node, target_time)

    # Plot the counts for the specified nodeID
    plot_file_path = f'satellite_counts_node_{args.plot_node_id}.txt'
    plot_counts(args.plot_node_id, plot_file_path)

if __name__ == "__main__":
    main()
