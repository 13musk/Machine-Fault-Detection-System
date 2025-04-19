import pandas as pd
import itd  

# Load synthetic vibration data
df = pd.read_csv("synthetic_vibration_data.csv")

# Apply ITD on the "Normal" signal
prc_output = itd.itd(df["Normal"].values)

# Check the length of each ITD component (for debugging)
for i in range(6):
    print(f"Component {i+1} Length: {len(prc_output[i])}")

# Select the last component as PRC (
prc_fixed = prc_output[-1]  

# Store PRC components in a DataFrame
prc_df = pd.DataFrame({
    "Time": df["Time"],
    "PRC_Normal": prc_fixed
})

# Save to CSV
prc_df.to_csv("prc_components.csv", index=False)
print("PRC Components saved successfully!")
