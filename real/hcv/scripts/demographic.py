import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('../data/output_results.csv')

# Extract data columns
time = data['Time']
mean = data['Mean']
median = data['Median']
lower95 = data['Lower95']
upper95 = data['Upper95']

# Set whether to use a log y-axis
use_log_scale = True  # True for log scale

# Option to set the earliest date
set_earliest_date = True
earliest_date = 1994

if set_earliest_date:
    # Adjust the time axis based on the earliest_date
    time = earliest_date - time
else:
    time = time - time.min()

# Plot mean and confidence interval
plt.figure(figsize=(10, 6))
plt.plot(time, mean, label='Mean Population Size')
plt.fill_between(time, lower95, upper95, color='b', alpha=0.2, label='95% HPD Interval')

# Plot median (optional)
plt.plot(time, median, label='Median Population Size', linestyle='--')

# Set the y-axis scale to logarithmic if needed
if use_log_scale:
    plt.yscale('log')

# Set axis labels and title
plt.xlabel('Time')
plt.ylabel('Population Size')
plt.title('Demographic History log scale')
plt.legend()

# Optional: invert x-axis if time is "years ago" style
# plt.gca().invert_xaxis()

manual_ticks = [10**i for i in range(2, 6)]  # 10^2, 10^3, 10^4, 10^5
plt.yticks(manual_ticks, [f"$10^{i}$" for i in range(2, 6)])


plt.savefig('../real/hcv/figures/hcv.png',
            format='png', dpi=600, bbox_inches='tight')

# Finally, show the plot on screen
plt.show()
