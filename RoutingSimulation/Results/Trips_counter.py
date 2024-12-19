import os
import re

# Define the range for i and j
i_range = range(1, 13)  # 1 to 12
j_range = range(1, 4)   # 1 to 3

# Define the file naming pattern
file_pattern = "simulation{i}_{j}.log"

# Store results
vehicle_counts = {}  # To store vehicle IDs and distance counts
time_counts = {}     # To store time reports for vehicles

# Process each file
for i in i_range:
    for j in j_range:
        # Generate the filename
        file_name = file_pattern.format(i=i, j=j)
        print(f"Processing {file_name}...")

        # Initialize counters
        vehicle_count = 0

        try:
            # Open the file for reading
            with open(file_name, 'r') as file:
                for line in file:
                    line = line.strip()

                    # Check for travel time entries
                    if re.search(r"Travel time for Vehicle \d+ is \d+ steps\.", line):
                        vehicle_count += 1

            # Store the results
            vehicle_counts[file_name] = vehicle_count

        except FileNotFoundError:
            print(f"File not found: {file_name}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

# Report results
print("\nSummary of Vehicle Counts in Log Entries:")
print(f"{'File Name':<25}{'Vehicles Count':<20}{'Travel Time Reports'}")
for file_name in sorted(vehicle_counts.keys()):
    print(f"{file_name:<25}{vehicle_counts[file_name]:<20}{vehicle_counts[file_name]}")

# Verify if each file has 19,200 vehicles
print("\nVerification:")
for file_name in sorted(vehicle_counts.keys()):
    vehicle_count = vehicle_counts.get(file_name, 0)

    if vehicle_count != 19200:
        print(f"{file_name}: Incomplete data! Vehicles Count = {vehicle_count}")
    else:
        print(f"{file_name}: Data verified, 19,200 vehicles counted.")
