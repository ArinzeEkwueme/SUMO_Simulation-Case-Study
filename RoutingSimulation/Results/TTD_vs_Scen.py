import matplotlib.pyplot as plt

# Data
scen = ["0%", "10%", "20%", "50%", "80%", "100%"]
ttt_cavre0_5 = [76165.80, 74201.84, 73723.83, 68018.93, 63619.22, 61764.25]
ttt_cavre1_0 = [74795.55, 74291.23, 74298.23, 66782.26, 63312.48, 62084.69]

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
