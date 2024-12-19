import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Labels for scenarios
labels = [
    "0% (0.5)", "0% (1.0)", "10% (0.5)", "10% (1.0)",
    "20% (0.5)", "20% (1.0)", "50% (0.5)", "50% (1.0)",
    "80% (0.5)", "80% (1.0)", "100% (0.5)", "100% (1.0)"
]

# Colors for labels
colors = ['cyan' if '(0.5)' in label else 'orange' for label in labels]

# Container for storing distance data for each scenario
scenario_data = []

# List to store scenario statistics
output_data = []

# Process files for each scenario
for i in range(1, 13):  # Scenarios 1 to 12
    distances = []
    for j in range(1, 4):  # Sub-scenarios 1 to 3
        file_name = f'Vehicle_distances/vehicle_distances{i}_{j}.csv'
        try:
            # Read the CSV file
            data = pd.read_csv(file_name)
            
            # Ensure the file has the correct structure
            if 'distance_travelled' not in data.columns:
                raise ValueError(f"Column 'distance_travelled' not found in {file_name}")
            
            # Convert distances to kilometers and append to the list
            distances.extend(data['distance_travelled'] / 1000)  # Convert meters to kilometers
        except Exception as e:
            output_data.append({
                "Scenario": i,
                "Sub-scenario": j,
                "Error": str(e),
                "Avg Distance (km)": None,
                "25th Percentile (km)": None,
                "75th Percentile (km)": None
            })

    # Calculate statistics if data is available
    if distances:
        avg_distance = np.mean(distances)
        p25 = np.percentile(distances, 25)
        p75 = np.percentile(distances, 75)
    else:
        avg_distance, p25, p75 = 0, 0, 0

    # Add distances to the scenario data
    scenario_data.append(distances)

    # Add scenario statistics to the output
    output_data.append({
        "Scenario": i,
        "Sub-scenario": "All",
        "Error": None,
        "Avg Distance (km)": avg_distance,
        "25th Percentile (km)": p25,
        "75th Percentile (km)": p75
    })

# Save the results to a CSV file
output_df = pd.DataFrame(output_data)
output_df.to_csv('vehicle_distances_statistics.csv', index=False)

# Create the box plot
plt.figure(figsize=(12, 8))
box = plt.boxplot(scenario_data, patch_artist=True, labels=labels, showfliers=False)

# Apply colors to the boxes
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Create legend
legend_handles = [
    Patch(facecolor='cyan', edgecolor='black', label='CAVRePr=0.5'),
    Patch(facecolor='orange', edgecolor='black', label='CAVRePr=1.0')
]
plt.legend(handles=legend_handles, loc='upper right', fontsize=12)

# Add title, axis labels, and grid
plt.title('Box Plot of Vehicle Distances vs Scenarios')
plt.xlabel('Scenarios')
plt.ylabel('Vehicle Distances (kilometers)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the plot
plt.savefig('vehicle_distances_boxplot_km.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
