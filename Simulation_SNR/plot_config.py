import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.sans-serif'] = ['Times New Roman']

linewidth = 3
xyfontsize = 30
figsize = (10, 6)
tick_size = 25
legend_size = 20
alpha = 0.1
annotation_fontsize = 20

plt.rcParams['axes.labelsize'] = xyfontsize
plt.rcParams['xtick.labelsize'] = tick_size
plt.rcParams['ytick.labelsize'] = tick_size
plt.rcParams['legend.fontsize'] = legend_size
plt.rcParams['figure.figsize'] = figsize
plt.rcParams['lines.linewidth'] = linewidth
plt.rcParams["xtick.direction"] = "out"
plt.rcParams["ytick.direction"] = "out"
hatches = ['||', '\\\\', '//', '-','.', '+', 'x', 'o', 'O', '*', '.', '||']

experiment_colors = [
    '#1f77b4',  # muted blue
    '#2ca02c',  # muted green
    '#d62728',  # muted red
    '#ff7f0e',  # muted orange
    '#9467bd',  # muted purple
    '#8c564b',  # muted brown
    '#e377c2',  # muted pink
    '#7f7f7f',  # muted gray
    '#bcbd22',  # muted olive
    '#17becf'   # muted cyan
]

linestyle_list = ['solid', 'dotted', 'dashed', 'dashdot', (0, (5, 1)), (0, (3, 1, 1, 1, 1, 1)), (0, (3, 1, 1, 1, 1, 1))]

