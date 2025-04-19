import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_results():
    """
    Plot the PRC signal and feature values
    """
    # Load the data
    prc_df = pd.read_csv("prc_components.csv")
    features_df = pd.read_csv("prc_features.csv")
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot PRC signal
    ax1.plot(prc_df["Time"], prc_df["PRC_Normal"], label="PRC Signal")
    ax1.set_title("PRC Signal")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)
    ax1.legend()
    
    # Plot feature values
    features_to_plot = ["RMS", "Kurtosis", "Crest Factor", "Standard Deviation"]
    values = [features_df[feature].iloc[0] for feature in features_to_plot]
    ax2.bar(features_to_plot, values)
    ax2.set_title("Feature Values")
    ax2.set_ylabel("Value")
    ax2.grid(True)
    
    # Add thresholds
    thresholds = {
        "RMS": 0.1,
        "Kurtosis": 3.0,
        "Crest Factor": 2.5,
        "Standard Deviation": 0.15
    }
    
    for i, feature in enumerate(features_to_plot):
        ax2.axhline(y=thresholds[feature], color='r', linestyle='--', alpha=0.5)
        ax2.text(i, thresholds[feature], f"Threshold: {thresholds[feature]:.2f}", 
                 ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig("fault_detection_results.png")
    print("Results plotted and saved to fault_detection_results.png ✅")

if __name__ == "__main__":
    plot_results() 