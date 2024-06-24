import matplotlib.pyplot as plt
import re
import plot_config

# Function to read the scores from the log file
def read_scores(log_file):
    scores = []
    with open(log_file, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:  # Skip the first line
            parts = line.split(': ')
            phase = parts[0].strip()
            score = float(parts[1].strip())
            scores.append((phase, score))
    return scores

# Function to extract numerical part from the phase file name
def extract_number(phase_file):
    match = re.search(r'phase_(\d+)_sorted', phase_file)
    if match:
        return match.group(1)
    return phase_file

# Function to plot the scores
def plot_scores(scores):
    phases = [extract_number(score[0]) for score in scores]
    values = [score[1] for score in scores]

    plt.figure(figsize=(10, 6))
    plt.plot(phases, values, marker='o')
    plt.xlabel('Satellite Number')
    plt.ylabel('Total Objective Function Score')
    # plt.title('Total Score for Each Phase File')
    plt.xticks(rotation=90)
    plt.tight_layout()
    # plt.show()
    plt.savefig("plot_objective_function_score_plus1_phase_24.png")

# Main script
log_file = 'objective_function_log.txt'
scores = read_scores(log_file)
plot_scores(scores)
