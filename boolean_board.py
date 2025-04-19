import pandas as pd
import numpy as np

def detect_fault(features):
    """
    Fault detection using available features: Mean, Max, Min, Std Dev, Variance
    """
    print("Available columns in features:", features.columns.tolist())

    # Extract features
    mean = features["Mean"].iloc[0]
    max_val = features["Max"].iloc[0]
    std = features["Standard Deviation"].iloc[0]
    var = features["Variance"].iloc[0]

    # Thresholds — update based on real observations
    MEAN_THRESHOLD = 0.05
    MAX_THRESHOLD = 0.1
    STD_THRESHOLD = 0.15
    VAR_THRESHOLD = 0.02

    # Fault logic
    if max_val > MAX_THRESHOLD and std > STD_THRESHOLD:
        return "Severe Fault"
    elif mean > MEAN_THRESHOLD or var > VAR_THRESHOLD:
        return "Warning"
    else:
        return "Normal"

# Load extracted features
df = pd.read_csv("prc_features.csv")

try:
    condition = detect_fault(df)

    print(f"\nMachine Condition: {condition}")
    print("\nFeature Values:")
    for feature in ["Mean", "Max", "Min", "Standard Deviation", "Variance"]:
        print(f"{feature}: {df[feature].iloc[0]:.4f}")

    with open("boolean_result.txt", "w") as f:
        f.write(f"Machine Condition: {condition}\n")
        f.write("\nFeature Values:\n")
        for feature in ["Mean", "Max", "Min", "Standard Deviation", "Variance"]:
            f.write(f"{feature}: {df[feature].iloc[0]:.4f}\n")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
