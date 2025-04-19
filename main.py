import pandas as pd
import numpy as np
from itd import itd
import matplotlib.pyplot as plt
from extract_features import extract_features
from boolean_board import detect_fault
from plot_results import plot_results

def main():
    # Step 1: Load vibration data
    print("Loading vibration data...")
    df = pd.read_csv("synthetic_vibration_data.csv")
    
    # Step 2: Apply ITD decomposition
    print("Applying ITD decomposition...")
    prc_output = itd(df["Normal"].values)
    prc_fixed = prc_output[-1]  # Get the last component as PRC
    
    # Save PRC components
    prc_df = pd.DataFrame({
        "Time": df["Time"],
        "PRC_Normal": prc_fixed
    })
    prc_df.to_csv("prc_components.csv", index=False)
    
    # Step 3: Extract features
    print("Extracting features...")
    features_df = extract_features()
    
    # Step 4: Detect faults using Boolean logic
    print("Detecting faults...")
    condition = detect_fault(features_df)
    
    # Step 5: Visualize results
    print("Generating visualization...")
    plot_results()
    
    print("\nFault Detection Complete!")
    print(f"Machine Condition: {condition}")

if __name__ == "__main__":
    main() 