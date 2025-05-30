"""Plot the position of each driver at the end of each lap."""

import matplotlib.pyplot as plt
import fastf1.plotting

# Load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

# Load the session and create the plot
session = fastf1.get_session(2025, 2, 'R')
session.load(telemetry=False, weather=False)
fig, ax = plt.subplots(figsize=(8.0, 4.9))

for driver in session.drivers:
    driver_laps = session.laps.pick_drivers(driver)
    abbreviation = driver_laps['Driver'].iloc[0]
    # get color of each driver
    style = fastf1.plotting.get_driver_style(identifier=abbreviation, style=['color', 'linestyle'], session=session)
    # plot driver's position over the number of laps
    ax.plot(driver_laps['LapNumber'], driver_laps['Position'], label=abbreviation, **style)

# setting y-limits that invert the y-axis so that position one is at the top
ax.set_ylim([20.5, 0.5])
ax.set_yticks([1, 5, 10, 15, 20])
ax.set_xlabel('Lap')
ax.set_ylabel('Position')

# add the legend outside the plot area
ax.legend(bbox_to_anchor=(1.0, 1.02))


plt.title(f"Position changes \n" f"{session.event.year} {session.event['EventName']}")
plt.tight_layout()
plt.show()