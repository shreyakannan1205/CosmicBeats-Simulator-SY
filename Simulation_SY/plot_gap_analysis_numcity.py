import matplotlib.pyplot as plt
import re
import os
from datetime import timedelta
import plot_config

def parse_duration(duration_str):
    """Parses a duration string into a timedelta object."""
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

def parse_gap_duration(file_path):
    """Extracts and averages the total gap durations from the file."""
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        
        total_gap_duration = timedelta()
        count = 0
        
        for line in content:
            match = re.search(r'Total gap duration: ((\d+ day[s]?, )?\d+:\d+:\d+\.\d+)', line)
            if match:
                duration_str = match.group(1).strip()
                total_gap_duration += parse_duration(duration_str)
                count += 1
        
        if count == 0:
            raise ValueError(f"No valid gap durations found in {file_path}")
        
        average_gap_duration = total_gap_duration / count
        return average_gap_duration
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return timedelta()

def calculate_idle_percentage(total_gap_duration, n, total_duration):
    """Calculates the percentage of idle time."""
    return (total_gap_duration / total_duration) * 100 - (n - 1) * 100

def main():
    total_duration = timedelta(days=7)  
    num_cities = []
    idle_percentages = []

    directory = "NumCity"
    max_cities = 21 

    for n in range(1, max_cities + 1):
        total_gap_duration = timedelta()
        for i in range(1, n + 1):
            file_index = 10000 + i
            file_path = os.path.join(directory, f"output_numcity_{n}_gap_duration_analysis_{file_index}.txt")
            average_gap_duration = parse_gap_duration(file_path)
            total_gap_duration += average_gap_duration
        
        idle_percentage = calculate_idle_percentage(total_gap_duration, n, total_duration)
        num_cities.append(n)
        idle_percentages.append(idle_percentage)
        print(f"Number of cities: {n}, Idle Percentage: {idle_percentage}")  

    # Plotting the data
    plt.figure(figsize = (10,6.1))
    plt.plot(num_cities, idle_percentages, marker='o')
    plt.xlabel('Number of Cities')
    plt.ylabel('Idle Time Percentage (%)')
    plt.grid(True)
    plt.xticks(range(1, max_cities + 1), fontsize = 22)

    y_ticks = range(88, 101, 2) 
    y_labels = [str(tick) for tick in y_ticks]
    plt.yticks(ticks=y_ticks, labels=y_labels)
    plt.tight_layout()
    plt.savefig("plot_gap_analysis_numcity.png")
    print("Plot saved as plot_gap_analysis_numcity.png") 

if __name__ == "__main__":
    main()
