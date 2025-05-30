'''Plot a driver’s lap times in a race, with color coding for the compounds.'''

import seaborn as sns
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
from matplotlib.ticker import FuncFormatter

# Enable Matplotlib patches for plotting timedelta values and load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

# load the race session
race = fastf1.get_session(2025, 2, 'R')
race.load()

# get all the laps under the green flag for a driver
DRIVER = 'HAM'
driver_laps = race.laps.pick_drivers(DRIVER).pick_accurate().reset_index()

# convert LapTime to total seconds for plotting
driver_laps['LapTimeSeconds'] = driver_laps['LapTime'].dt.total_seconds()

# function to format the y-axis labels as lap times
def format_lap_time(x, pos):
    minutes = int(x // 60)
    seconds = x % 60
    return f'{minutes}:{seconds:03.1f}'

# Make the scattterplot using lap number as x-axis and lap time as y-axis, marker colors correspond to the compounds used
fig, ax = plt.subplots()
sns.scatterplot(data=driver_laps,
                x="LapNumber",
                y="LapTimeSeconds",
                ax=ax,
                hue="Compound",
                palette=fastf1.plotting.get_compound_mapping(session=race),
                s=80,
                linewidth=0,
                legend='auto')

# format the y-axis labels as lap times
ax.yaxis.set_major_formatter(FuncFormatter(format_lap_time))
ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")

plt.title(f"{DRIVER} Laptimes \n {race.event.year} {race.event['EventName']}")
plt.grid(color='w', which='major', axis='both')
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()