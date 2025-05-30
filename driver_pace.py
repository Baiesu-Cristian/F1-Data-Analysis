'''Rank team’s race pace from the fastest to the slowest.'''

import seaborn as sns
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
from matplotlib.ticker import FuncFormatter


# Load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

# load the race sessions and pick only the laps under green flag
race = fastf1.get_session(2025, 2, 'R')
race.load()
laps = race.laps.pick_accurate()

# Convert the lap time column from timedelta to integer
transformed_laps = laps.copy()
transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

# filter out drivers who completed less than half the race
total_laps = race.total_laps
laps_completed = transformed_laps.groupby("Driver")["LapNumber"].count()
drivers_to_include = laps_completed[laps_completed >= total_laps / 2].index
filtered_laps = transformed_laps[transformed_laps["Driver"].isin(drivers_to_include)]

# order the teams and drivers by their median lap times
driver_order = (filtered_laps[["Driver", "LapTime (s)"]].groupby("Driver").median()["LapTime (s)"].sort_values().index)

# Calculate the fastest median lap time for teams and drivers
fastest_driver_time = filtered_laps.groupby("Driver")["LapTime (s)"].median().min()

# Add the time difference to the x-axis labels for drivers
driver_order_with_diff = [
    f"{driver}\n+{(filtered_laps[filtered_laps['Driver'] == driver]['LapTime (s)'].median() - fastest_driver_time):.2f}"
    for driver in driver_order
]

# function to format the y-axis labels as lap times
def format_lap_time(x, pos):
    minutes = int(x // 60)
    seconds = x % 60
    return f'{minutes}:{seconds:03.1f}'

# make a color palette associating team and driver names to hex codes
driver_palette = {driver: fastf1.plotting.get_driver_color(driver, session=race) for driver in driver_order}

fig, ax2 = plt.subplots()

# driver pace plot
sns.boxplot(
    data=filtered_laps,
    x="Driver",
    y="LapTime (s)",
    hue="Driver",
    order=driver_order,
    palette=driver_palette,
    whiskerprops=dict(color="white"),
    boxprops=dict(edgecolor="white"),
    medianprops=dict(color="grey"),
    capprops=dict(color="white"),
    ax=ax2
)
ax2.set_title(f"{race.event.year} {race.event['EventName']} \n Driver Pace", fontsize=12)
ax2.grid(visible=False)
ax2.set(xlabel=None)
ax2.set_xticks(range(len(driver_order)))
ax2.set_xticklabels(driver_order_with_diff)
ax2.yaxis.set_major_formatter(FuncFormatter(format_lap_time))
ax2.tick_params(axis="x", labelsize=8)

plt.tight_layout()
plt.show()