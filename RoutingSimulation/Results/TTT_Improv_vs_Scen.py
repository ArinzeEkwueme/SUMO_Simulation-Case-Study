import matplotlib.pyplot as plt

# Data
cav_pr = ["0%", "10%", "20%", "50%", "80%", "100%"]
ttt_cavre0_5 = [(93269870+70412130+)/3, (20844981+67447314+)/3, (67422625+62714972+41331039)/3, (8534510+8376738+8718363)/3, (5611322+5580657+5593618)/3, (5045089+5054373+5049557)/3]
ttt_cavre1_0 = [(105416014+60632795+)/3, (86469388++)/3, (63265357+20870941+57491148)/3, (8314839+7927077+8104793)/3, (5545793+5567973+5587960)/3, (5162365+5183772+5166100)/3]

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
