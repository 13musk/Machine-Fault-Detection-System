import pandas as pd
import numpy as np
from scipy import stats

def calculate_features(signal):
    """
    Calculate statistical features from a signal
    """
    features = {
        "Mean": np.mean(signal),
        "Max": np.max(signal),
        "Min": np.min(signal),
        "Standard Deviation": np.std(signal),
        "Variance": np.var(signal),
        "RMS": np.sqrt(np.mean(signal**2)),
        "Kurtosis": stats.kurtosis(signal),
        "Skewness": stats.skew(signal),
        "Peak to Peak": np.max(signal) - np.min(signal),
        "Crest Factor": np.max(signal) / np.sqrt(np.mean(signal**2))
    }
    return features

def extract_features():
    """
    Extract features from PRC components
    """
    # Load the PRC component data
    df = pd.read_csv("prc_components.csv")
    
    # Extract the PRC signal
    prc_signal = df["PRC_Normal"]
    
    # Calculate features
    features = calculate_features(prc_signal)
    
    # Convert to DataFrame
    features_df = pd.DataFrame([features])
    
    # Save to CSV
    features_df.to_csv("prc_features.csv", index=False)
    print("Enhanced features extracted and saved to prc_features.csv ✅")
    
    return features_df

if __name__ == "__main__":
    extract_features()
