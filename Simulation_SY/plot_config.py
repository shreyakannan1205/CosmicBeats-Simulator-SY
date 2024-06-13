import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']

linewidth = 3
xyfontsize = 20
figsize = (10, 6)
tick_size = 18
legend_size = 20
alpha = 0.1
annotation_fontsize = 15

plt.rcParams['axes.labelsize'] = xyfontsize
plt.rcParams['xtick.labelsize'] = tick_size
plt.rcParams['ytick.labelsize'] = tick_size
plt.rcParams['legend.fontsize'] = legend_size
plt.rcParams['figure.figsize'] = figsize
plt.rcParams['lines.linewidth'] = linewidth
plt.rcParams["xtick.direction"] = "out"
plt.rcParams["ytick.direction"] = "out"
hatches = ['.', '||', '\\\\', '//', '-', '+', 'x', 'o', 'O', '*', '.', '||']

experiment_colors = [
    'lightblue', 'lightpink', 'lightgreen', 'lightyellow', 'lightgrey',
    'peachpuff', 'floralwhite', 'lightcoral', 'lightgoldenrodyellow', 'lightcyan',
    'lavender', 'honeydew', 'mintcream', 'azure', 'aliceblue', 'mistyrose'
]

linestyle_list = ['solid', 'dotted', 'dashed', 'dashdot', (0, (5, 1)), (0, (3, 1, 1, 1, 1, 1)), (0, (3, 1, 1, 1, 1, 1))]

def plot_cdf(data, linestyle='none', label='none'):
    data_sorted = np.sort(data)
    cdf = np.linspace(0, 1, len(data))
    plt.plot(data_sorted, cdf,  linestyle=linestyle, label=label)
