import matplotlib.pyplot as plt

# Data
cav_pr = ["0%", "10%", "20%", "50%", "80%", "100%"]
ttt_cavre0_5 = [73357578, 62702691, 57156212, 8543204, 5595199, 5049673]
ttt_cavre1_0 = [91682991, 84651016, 51629826, 8115569, 5567242, 5170745]

# Plot
plt.figure(figsize=(8, 6))
plt.plot(cav_pr, ttt_cavre0_5, marker='o', label='CAVRePr=0.5', linewidth=2)
plt.plot(cav_pr, ttt_cavre1_0, marker='s', label='CAVRePr=1.0', linewidth=2)

# Labels and Title
plt.title("Total Travel Time vs Simulation Scenarios", fontsize=16)
plt.xlabel("Simulation Scenarios", fontsize=14)
plt.ylabel("Total Travel Time (seconds)", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# Show Plot
plt.savefig("ttt_vs_scen.jpg", dpi=300)  # Save the plot as a high-resolution image
plt.show()
