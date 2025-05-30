'''Compare two drivers' fastest laps by overlaying their speed traces.'''

import matplotlib.pyplot as plt
import fastf1.plotting

# Enable Matplotlib patches for plotting timedelta values and load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

# load a session and its telemetry data
session = fastf1.get_session(2025, 2, 'Q')
session.load()

# select the two drivers to compare
DRIVER1 = 'LEC'
DRIVER2 = 'HAM'
lap1 = session.laps.pick_drivers(DRIVER1).pick_fastest()
lap2 = session.laps.pick_drivers(DRIVER2).pick_fastest()

# get the telemetry data for each lap and add "Distance" coloumn to the telemetry dataframe to make it easier to compare laps
tel1 = lap1.get_car_data().add_distance()
tel2 = lap2.get_car_data().add_distance()

# get the driver's team's color
color1 = fastf1.plotting.get_team_color(lap1['Team'], session=session)
color2 = fastf1.plotting.get_team_color(lap2['Team'], session=session)
if color1 == color2:
    color1 = 'red'
    color2 = 'blue'

# plot speed traces and throttle traces
fig, (ax1, ax2) = plt.subplots(2, 1)

# Speed plot
ax1.plot(tel1['Distance'], tel1['Speed'], color=color1, label=f"{DRIVER1} ({str(lap1['LapTime'])[11:19]})")
ax1.plot(tel2['Distance'], tel2['Speed'], color=color2, label=f"{DRIVER2} ({str(lap2['LapTime'])[11:19]})")
ax1.set_ylabel('Speed in km/h')
ax1.legend()

# Throttle plot
ax2.plot(tel1['Distance'], tel1['Throttle'], color=color1, label=f"{DRIVER1} ({str(lap1['LapTime'])[11:19]})")
ax2.plot(tel2['Distance'], tel2['Throttle'], color=color2, label=f"{DRIVER2} ({str(lap2['LapTime'])[11:19]})")
ax2.set_xlabel('Distance in m')
ax2.set_ylabel('Throttle %')
ax2.legend()

fig.suptitle(f"Fastest Lap Comparison \n" f"{session.event.year} {session.event['EventName']} {session.name}")
plt.show()