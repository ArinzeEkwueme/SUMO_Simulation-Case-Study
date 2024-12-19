import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd

# Define the labels as specified
labels = [
    "0% (0.5)", "0% (1.0)", "10% (0.5)", "10% (1.0)",
    "20% (0.5)", "20% (1.0)", "50% (0.5)", "50% (1.0)",
    "80% (0.5)", "80% (1.0)", "100% (0.5)", "100% (1.0)"
]

# Define the colors
colors = ['cyan' if '(0.5)' in label else 'orange' for label in labels]

# Container for storing travel times for each scenario
scenario_data = []

# List to store scenario statistics
output_data = []

# Process log files
for i in range(1, 13):  # Scenarios 1 to 12
    travel_times = []
    for j in range(1, 4):  # Sub-scenarios 1 to 3
        log_file_name = f'Simulation_log/Simulation{i}_{j}.log'
        try:
            with open(log_file_name, 'r') as file:
                for line in file:
                    # Match lines containing travel time data
                    match = re.search(r'INFO:Strategy:Travel time for Vehicle .* is (\d+) steps', line)
                    if match:
                        travel_time = int(match.group(1))
                        travel_times.append(travel_time)
        except Exception as e:
            output_data.append({
                "Scenario": i,
                "Sub-scenario": j,
                "Error": str(e),
                "Avg Travel Time (steps)": None,
                "25th Percentile (steps)": None,
                "75th Percentile (steps)": None
            })

    # Calculate statistics
    if travel_times:
        avg_time = np.mean(travel_times)
        p25 = np.percentile(travel_times, 25)
        p75 = np.percentile(travel_times, 75)
    else:
        avg_time, p25, p75 = 0, 0, 0

    # Add scenario statistics to the output
    output_data.append({
        "Scenario": i,
        "Sub-scenario": "All",
        "Error": None,
        "Avg Travel Time (steps)": avg_time,
        "25th Percentile (steps)": p25,
        "75th Percentile (steps)": p75
    })

    # Add to the scenario data
    scenario_data.append(travel_times)

# Save the results to a CSV file
output_df = pd.DataFrame(output_data)
output_df.to_csv('travel_times_statistics.csv', index=False)

# Create the box plot
plt.figure(figsize=(12, 8))

# Create the box plot and apply colors
box = plt.boxplot(scenario_data, patch_artist=True, labels=labels, showfliers=False)

for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Add legend
legend_handles = [
    Patch(facecolor='cyan', edgecolor='black', label='CAVRePr=0.5'),
    Patch(facecolor='orange', edgecolor='black', label='CAVRePr=1.0')
]
plt.legend(handles=legend_handles, loc='upper right', fontsize=12)

# Add title, axis labels, and grid
plt.title('Box Plot of Vehicle Travel Times vs Scenarios')
plt.xlabel('Scenarios')
plt.ylabel('Travel Times (seconds)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the plot
plt.savefig('travel_times_boxplot_updated.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
