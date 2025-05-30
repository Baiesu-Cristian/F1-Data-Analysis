'''Rank team’s race pace from the fastest to the slowest.'''

import seaborn as sns
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
from matplotlib.ticker import FuncFormatter

# Load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

# load the race sessions and pick only the laps under green flag
race = fastf1.get_session(2025, 1, 'R')
race.load()
laps = race.laps.pick_accurate()

# Convert the lap time column from timedelta to integer
transformed_laps = laps.copy()
transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

# order the teams and drivers by their median lap times
team_order = (transformed_laps[["Team", "LapTime (s)"]].groupby("Team").median()["LapTime (s)"].sort_values().index)\

# Calculate the fastest median lap time for teams and drivers
fastest_team_time = transformed_laps.groupby("Team")["LapTime (s)"].median().min()\

# Add the time difference to the x-axis labels for teams
team_order_with_diff = [
    f"{team}\n+{(transformed_laps[transformed_laps['Team'] == team]['LapTime (s)'].median() - fastest_team_time):.2f}"
    for team in team_order
]

# function to format the y-axis labels as lap times
def format_lap_time(x, pos):
    minutes = int(x // 60)
    seconds = x % 60
    return f'{minutes}:{seconds:03.1f}'

# make a color palette associating team and driver names to hex codes
team_palette = {team: fastf1.plotting.get_team_color(team, session=race) for team in team_order}\

fig, ax1 = plt.subplots()

# team pace plot
sns.boxplot(
    data=transformed_laps,
    x="Team",
    y="LapTime (s)",
    hue="Team",
    order=team_order,
    palette=team_palette,
    whiskerprops=dict(color="white"),
    boxprops=dict(edgecolor="white"),
    medianprops=dict(color="grey"),
    capprops=dict(color="white"),
    ax=ax1
)
ax1.set_title(f"{race.event.year} {race.event['EventName']} \n Team Pace", fontsize=12)
ax1.grid(visible=False)
ax1.set(xlabel=None)
ax1.set_xticks(range(len(team_order)))
ax1.set_xticklabels(team_order_with_diff)
ax1.yaxis.set_major_formatter(FuncFormatter(format_lap_time))
ax1.tick_params(axis="x", labelsize=8)

plt.tight_layout()
plt.show()