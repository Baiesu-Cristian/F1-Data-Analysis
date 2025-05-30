'''Plot all drivers’ tyre strategies during a race.'''

from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

# load the race session and laps
session = fastf1.get_session(2025, 2, 'R')
session.load()
laps = session.laps

# get the list of driver numbers
drivers = session.drivers

# Convert the driver numbers to three letter abbreviations
drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]

# to find the stint length and compound used for every stint by every driver, we group the laps by the driver, the stint number, and the compound. And then counting the number of laps in each group.
stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
stints = stints.groupby(["Driver", "Stint", "Compound"])
stints = stints.count().reset_index()

# The number in the LapNumber column now stands for the number of observations in that group aka the stint length.
stints = stints.rename(columns={"LapNumber": "StintLength"})

# plot the strategies for each driver
fig, ax = plt.subplots(figsize=(5, 10))

for driver in drivers:
    driver_stints = stints.loc[stints["Driver"] == driver]
    previous_stint_end = 0
    for idx, row in driver_stints.iterrows():
        compound_color = fastf1.plotting.get_compound_color(row["Compound"], session=session)
        plt.barh(
            y=driver,
            width=row["StintLength"],
            left=previous_stint_end,
            color=compound_color,
            edgecolor="black",
            fill=True
        )
        previous_stint_end += row["StintLength"]

plt.title(f"{session.event.year} {session.event['EventName']} Strategies")
plt.xlabel("Lap Number")
plt.grid(False)
# invert the y-axis so drivers that finish higher are closer to the top
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.show()