import fastf1.core
from helper_functions.telemetry.lap_telemetry import get_session_top_speeds
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.colors import Normalize
import numpy.ma as ma
import os

def plot_session_top_n_speeds(session: fastf1.core.Session, top_n: int = 15):
    top_speeds_dict = get_session_top_speeds(session, top_n)
    sorted_top_speeds_dict = sorted(top_speeds_dict.items(), key=lambda x: x[1][0][0], reverse=True)
    sorted_top_speeds = list(map(lambda x: list(map(lambda y: y[0], x[1])), sorted_top_speeds_dict))
    sorted_driver_abbreviations = list(map(lambda x: session.get_driver(x[0])['Abbreviation'], sorted_top_speeds_dict))
    sorted_drs_statuses = list(map(lambda x: list(map(lambda y: y[1], x[1])), sorted_top_speeds_dict))

    # Convert data to numpy array and mask -1 values
    speeds_array = np.array(sorted_top_speeds)
    masked_speeds = ma.masked_where(speeds_array == -1, speeds_array)

    # Create a custom colormap where the lowest value (-1 in this case) is transparent
    cmap = plt.cm.viridis
    cmap.set_bad(color='grey', alpha=0.5)  # Masked values will appear in grey

    # Normalize ignoring -1 values
    norm = Normalize(vmin=masked_speeds.min(), vmax=masked_speeds.max())

    fig, ax = plt.subplots()
    im = ax.imshow(masked_speeds, cmap=cmap, norm=norm)

    ax.set_yticks(np.arange(len(sorted_driver_abbreviations)), labels=sorted_driver_abbreviations)

    for i in range(len(sorted_top_speeds)):
        for j in range(len(sorted_top_speeds[i])):
            if sorted_top_speeds[i][j] == -1:
                ax.text(j, i, 'N/A', ha='center', va='center', color='w')
            else:
                ax.text(j, i, sorted_top_speeds[i][j], ha='center', va='center', color='w')

    for i in range(len(sorted_drs_statuses)):
        for j in range(len(sorted_drs_statuses[i])):
            if sorted_drs_statuses[i][j]:
                rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor='w', lw=2)
                ax.add_patch(rect)

    session_info = session.session_info
    title = f"{session_info['Meeting']['Name']} {session_info['StartDate'].year} - {session_info['Name']} - Top Speed (km/h) for Each Lap"

    # Hide axes, but keep y-tick labels
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks_position('none')

    # Add text at the bottom of the plot
    bottom_text = "Laps Sorted by Maximum Speed (15 Best Shown). \n White Borders Indicate DRS Usage."
    plt.figtext(0.5, 0.08, bottom_text, ha='center', va='center')

    fig.set_size_inches(18, 9)
    plt.title(title)
    if session.api_path:
        os.makedirs(f"../../storage/plots/{session.api_path}", exist_ok=True)
    plt.savefig(f"../../storage/plots/{session.api_path}/n_top_speeds.png")
