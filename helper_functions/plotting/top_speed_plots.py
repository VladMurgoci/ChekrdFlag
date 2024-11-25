import fastf1.core
from PIL.ImageColor import colormap
from fastf1.plotting import get_driver_color, get_team_color
from helper_functions.telemetry.lap_telemetry import get_session_driver_top_speeds, get_session_team_top_1_speeds
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.colors import Normalize
import numpy.ma as ma
import os

def plot_session_driver_top_n_speeds(session: fastf1.core.Session, top_n: int = 15):
    top_speeds_dict = get_session_driver_top_speeds(session, top_n)
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

    fig.set_size_inches(12, 12)
    plt.title(title)
    if session.api_path:
        os.makedirs(f"../../storage/plots/{session.api_path}", exist_ok=True)
    plt.savefig(f"../../storage/plots/{session.api_path}/n_top_speeds.png")

def plot_session_driver_top_speeds(session: fastf1.core.Session):
    top_speeds_dict = get_session_driver_top_speeds(session, 1)
    sorted_top_speeds_dict = sorted(top_speeds_dict.items(), key=lambda x: x[1][0][0], reverse=True)
    sorted_top_speeds = list(map(lambda x: x[1][0][0], sorted_top_speeds_dict))
    sorted_driver_abbreviations = list(map(lambda x: session.get_driver(x[0])['Abbreviation'], sorted_top_speeds_dict))
    sorted_drs_statuses = list(map(lambda x: x[1][0][1], sorted_top_speeds_dict))

    # Set driver colors
    driver_colors = []
    for i in range(len(sorted_driver_abbreviations)):
        driver_colors.append(get_driver_color(sorted_driver_abbreviations[i], session))

    # Create bar chart
    fig, ax = plt.subplots()
    ax.bar(sorted_driver_abbreviations, sorted_top_speeds, color=driver_colors)
    ax.set_title(f"{session.session_info['Meeting']['Name']} {session.session_info['StartDate'].year} - {session.session_info['Name']} - Top Speed (km/h)")
    ax.set_ylim(sorted_top_speeds[-1] - 10, sorted_top_speeds[0] + 10)

    # Add DRS usage indicator
    for i in range(len(sorted_drs_statuses)):
        if sorted_drs_statuses[i]:
            ax.text(i, sorted_top_speeds[i] - 10, 'DRS', ha='center', va='center', color='black')

    # Add text at top of each bar with speed
    for i in range(len(sorted_top_speeds)):
        ax.text(i, sorted_top_speeds[i] + 0.5 , sorted_top_speeds[i], ha='center', va='center', color='black')

    # Remove axis spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Remove y-axis
    ax.yaxis.set_ticks([])

    fig.set_size_inches(12, 12)
    if session.api_path:
        os.makedirs(f"../../storage/plots/{session.api_path}", exist_ok=True)
    plt.savefig(f"../../storage/plots/{session.api_path}/top_speeds.png")


def plot_session_team_top_speeds(session: fastf1.core.Session):
    team_top_speeds = get_session_team_top_1_speeds(session)
    team_names = list(map(lambda x: x[0], team_top_speeds))
    top_speeds = list(map(lambda x: x[1][0], team_top_speeds))

    # Set team colors
    team_colors = []
    for i in range(len(team_names)):
        team_colors.append(get_team_color(team_names[i], session))

    # Create bar chart
    fig, ax = plt.subplots()
    ax.bar(team_names, top_speeds, color=team_colors)
    ax.set_title(f"{session.session_info['Meeting']['Name']} {session.session_info['StartDate'].year} - {session.session_info['Name']} - Top Speed (km/h) by Team")
    ax.set_ylim(top_speeds[-1] - 10, top_speeds[0] + 10)

    # Add text at top of each bar with speed
    for i in range(len(top_speeds)):
        ax.text(i, top_speeds[i] + 0.5, top_speeds[i], ha='center', va='center', color='black')

    # Remove axis spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Remove y-axis
    ax.yaxis.set_ticks([])

    fig.set_size_inches(12, 12)
    if session.api_path:
        os.makedirs(f"../../storage/plots/{session.api_path}", exist_ok=True)
    plt.savefig(f"../../storage/plots/{session.api_path}/team_top_speeds.png")