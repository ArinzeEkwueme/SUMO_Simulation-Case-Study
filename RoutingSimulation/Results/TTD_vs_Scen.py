import matplotlib.pyplot as plt

# Data
scen = ["0%", "10%", "20%", "50%", "80%", "100%"]
ttt_cavre0_5 = [76465070, 76807146, 74148409, 70046431, 64874145, 62849207]
ttt_cavre1_0 = [77961795, 74322131, 73599208, 67984205, 63383231, 62092218]

# Plot
plt.figure(figsize=(8, 6))
plt.plot(scen, ttt_cavre0_5, marker='o', label='CAVRePr=0.5', linewidth=2)
plt.plot(scen, ttt_cavre1_0, marker='s', label='CAVRePr=1.0', linewidth=2)

# Labels and Title
plt.title("Total Travel Distance vs Simulation Scenarios", fontsize=16)
plt.xlabel("Simulation Scenarios", fontsize=14)
plt.ylabel("Total Travel Distance (kilometers)", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# Show Plot
plt.savefig("ttd_vs_scen.jpg", dpi=300)  # Save the plot as a high-resolution image
plt.show()
