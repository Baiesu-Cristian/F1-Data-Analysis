"""Plot the qualifying result with visualization the fastest times."""

import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import fastf1
import fastf1.plotting
from fastf1.core import Laps
from matplotlib.ticker import FuncFormatter

# Enable Matplotlib patches for plotting timedelta values
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme=None)

# load session data
session = fastf1.get_session(2025, 2, 'Q')
session.load()

# First, we need to get an array of all drivers.
drivers = pd.unique(session.laps['Driver'])

# we get each driver's fastest lap, create a new laps object from these laps, sort them by lap time and have reindex them by starting position.
list_fastest_laps = list()
for drv in drivers:
    drvs_fastest_lap = session.laps.pick_drivers(drv).pick_fastest()
    list_fastest_laps.append(drvs_fastest_lap)
fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

# plot only the time differences
pole_lap = fastest_laps.pick_fastest()
fastest_laps['LapTimeDelta'] = (fastest_laps['LapTime'] - pole_lap['LapTime']).dt.total_seconds()

# we create a list of team colors per lap to color our plot.
team_colors = list()
for index, lap in fastest_laps.iterlaps():
    color = fastf1.plotting.get_team_color(lap['Team'], session=session)
    team_colors.append(color)

# plot all the data
fig, ax = plt.subplots()
ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
        color=team_colors, edgecolor='grey')
ax.set_yticks(fastest_laps.index)
ax.set_yticklabels(fastest_laps['Driver'])

# Format the x-axis to show time differences as seconds with two decimal places
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.1f}"))

# show fastest at the top
ax.invert_yaxis()

# draw vertical lines behind the bars
ax.set_axisbelow(True)
ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

plt.suptitle(f" {session.event.year} {session.event['EventName']} Qualifying\n" f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

plt.show()
