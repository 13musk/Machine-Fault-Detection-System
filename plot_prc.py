import pandas as pd
import matplotlib.pyplot as plt

# Load the PRC data
prc_df = pd.read_csv("prc_components.csv")

# Apply Moving Average Smoothing
window_size = 10  # Adjust for smoother or sharper curves
prc_df["Smoothed_PRC"] = prc_df["PRC_Normal"].rolling(window=window_size, min_periods=1).mean()

# Plot the original and smoothed PRC component
plt.figure(figsize=(10, 5))
plt.plot(prc_df["Time"], prc_df["PRC_Normal"], label="Original PRC", color='b', linestyle='dashed')
plt.plot(prc_df["Time"], prc_df["Smoothed_PRC"], label="Smoothed PRC", color='r', linewidth=2)
plt.xlabel("Time")
plt.ylabel("PRC Value")
plt.title("Visualization of PRC Component (Smoothed)")
plt.legend()
plt.grid()
plt.show()
