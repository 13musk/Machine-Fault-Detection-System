import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
from itd import itd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Basic page setup                     
st.set_page_config(
    page_title="Machine Fault Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔧 Machine Fault Detection System")
st.markdown("""
### Understanding the Dataset
This application analyzes vibration data to detect machine faults using:
1. **ITD (Intrinsic Time-scale Decomposition)** to break down the signal
2. **Statistical Features** to characterize the signal
3. **Boolean Logic** to classify machine condition
""")

# File upload with example file hint
uploaded_file = st.file_uploader(
    "📂 Choose a CSV file",
    type=["csv"],
    help="Upload a CSV with time series vibration data (numeric values only)."
)

if uploaded_file:
    try:
        # Read the file
        content = uploaded_file.getvalue().decode('utf-8')
        
        # Check if file is empty
        if not content.strip():
            raise ValueError("The uploaded file is empty.")
            
        # Try to read the CSV with headers
        df = pd.read_csv(StringIO(content))
        
        # Data Overview Section
        st.header("📊 Data Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dataset Information")
            st.write(f"• Number of samples: {len(df)}")
            st.write(f"• Number of columns: {len(df.columns)}")
            st.write(f"• Column names: {', '.join(df.columns.tolist())}")
            
        with col2:
            st.subheader("Basic Statistics")
            st.dataframe(df.describe())
        
        # Handle different column names
        time_col = None
        vibration_col = None
        
        # Look for time column
        time_candidates = ['Time', 'time', 'TIME']
        for col in time_candidates:
            if col in df.columns:
                time_col = col
                break
                
        # Look for vibration column
        vibration_candidates = ['Vibration', 'vibration', 'VIBRATION', 'PRC_Normal', 'Signal']
        for col in vibration_candidates:
            if col in df.columns:
                vibration_col = col
                break
        
        if time_col is None:
            time_col = df.columns[0]
            
        if vibration_col is None:
            if len(df.columns) > 1:
                vibration_col = df.columns[1]
            else:
                raise ValueError("Could not identify vibration data column")
        
        # Create standardized DataFrame
        df_standard = pd.DataFrame({
            'Time': pd.to_numeric(df[time_col], errors='coerce'),
            'Vibration': pd.to_numeric(df[vibration_col], errors='coerce')
        })
        
        df = df_standard.dropna()
        
        # Data Visualization Section
        st.header("📈 Data Visualization")
        
        # Time Series Plot
        st.subheader("Raw Vibration Signal")
        fig_raw = px.line(df, x='Time', y='Vibration', title='Raw Vibration Signal Over Time')
        fig_raw.update_layout(height=400)
        st.plotly_chart(fig_raw, use_container_width=True)
        
        # Distribution Analysis
        st.subheader("Signal Distribution")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = px.histogram(df, x='Vibration', title='Vibration Amplitude Distribution')
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with col2:
            fig_box = px.box(df, y='Vibration', title='Vibration Amplitude Box Plot')
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Signal Statistics
        st.header("📊 Signal Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Mean Amplitude", f"{df['Vibration'].mean():.6f}")
            st.metric("Standard Deviation", f"{df['Vibration'].std():.6f}")
            
        with col2:
            st.metric("Maximum Amplitude", f"{df['Vibration'].max():.6f}")
            st.metric("Minimum Amplitude", f"{df['Vibration'].min():.6f}")
            
        with col3:
            st.metric("Signal Range", f"{df['Vibration'].max() - df['Vibration'].min():.6f}")
            st.metric("RMS Value", f"{np.sqrt(np.mean(df['Vibration']**2)):.6f}")
        
        # Sidebar for options
        with st.sidebar:
            st.header("⚙️ Analysis Parameters")
            n_components = st.slider("Number of ITD Components", 3, 10, 5)
            threshold_mean = st.slider("Mean Threshold", 0.0, 0.1, 0.05, 0.01)
            threshold_std = st.slider("Standard Deviation Threshold", 0.0, 0.3, 0.2, 0.01)

        # Perform ITD decomposition
        vibration_signal = df['Vibration'].values
        
        if len(vibration_signal) == 0:
            raise ValueError("Vibration signal is empty")
            
        # ITD Analysis Section
        st.header("🔄 ITD Decomposition")
        st.markdown("""
        ITD breaks down the signal into components:
        - Each component represents different time scales
        - Helps identify patterns and anomalies
        - Useful for fault detection
        """)
        
        H = itd(vibration_signal, N_max=n_components)
        
        # Calculate features for each component
        features = []
        for i, component in enumerate(H):
            features.append({
                'Component': f'PRC_{i+1}',
                'Mean': np.mean(component),
                'Std': np.std(component),
                'Max': np.max(component),
                'Min': np.min(component),
                'RMS': np.sqrt(np.mean(component**2))
            })
        
        features_df = pd.DataFrame(features)
        
        # Display component analysis
        st.subheader("Component Analysis")
        st.dataframe(features_df, use_container_width=True)

        # Plot components
        fig = make_subplots(rows=n_components+1, cols=1, 
                          subplot_titles=['Original Signal'] + [f'PRC {i+1}' for i in range(n_components)],
                          vertical_spacing=0.05)

        # Plot original signal
        fig.add_trace(go.Scatter(x=df['Time'], y=vibration_signal, name='Original'),
                     row=1, col=1)

        # Plot PRC components
        for i in range(n_components):
            fig.add_trace(go.Scatter(x=df['Time'], y=H[i], name=f'PRC {i+1}'),
                         row=i+2, col=1)

        fig.update_layout(height=200*(n_components+1), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Fault Detection Section
        st.header("🚨 Fault Detection")
        
        # Apply Boolean logic for fault detection
        mean_condition = features_df['Mean'].max() > threshold_mean
        std_condition = features_df['Std'].max() > threshold_std
        
        if mean_condition and std_condition:
            condition = "Faulty"
            color = "red"
        elif mean_condition or std_condition:
            condition = "Warning"
            color = "orange"
        else:
            condition = "Normal"
            color = "green"

        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Machine Condition")
            st.markdown(f"<h2 style='color: {color};'>{condition}</h2>", unsafe_allow_html=True)
            
            if condition == "Faulty":
                st.error("High vibration levels detected - Maintenance required")
            elif condition == "Warning":
                st.warning("Elevated vibration levels - Monitor closely")
            else:
                st.success("Normal operation - No action required")
            
        with col2:
            st.subheader("Detection Thresholds")
            st.write(f"Mean Threshold: {threshold_mean}")
            st.write(f"Std Dev Threshold: {threshold_std}")
            st.write(f"Max Mean: {features_df['Mean'].max():.4f}")
            st.write(f"Max Std Dev: {features_df['Std'].max():.4f}")

        # Download options
        st.header("📥 Download Results")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = features_df.to_csv(index=False)
            st.download_button(
                label="Download Features (CSV)",
                data=csv,
                file_name="features.csv",
                mime="text/csv"
            )
            
        with col2:
            html = fig.to_html()
            st.download_button(
                label="Download Plot (HTML)",
                data=html,
                file_name="decomposition_plot.html",
                mime="text/html"
            )

    except Exception as e:
        st.error(f"❗ Error processing file: {str(e)}")
        st.info("Please ensure your CSV file:")
        st.markdown("- Is not empty")
        st.markdown("- Has at least 10 data points")
        st.markdown("- Contains time series data and vibration measurements")
        st.markdown("- Contains only numeric values")
        st.markdown("- Has no extra headers or non-numeric rows")
        
        # Show example data format
        st.subheader("Example Data Format")
        st.markdown("Your file can have headers like:")
        st.code("Time,Vibration\n# or\nTime,PRC_Normal\n# or any similar column names")
        example_data = pd.DataFrame({
            'Time': [0.0, 0.1, 0.2, 0.3, 0.4],
            'Vibration': [0.1, 0.15, 0.12, 0.18, 0.14]
        })
        st.dataframe(example_data)
else:
    st.info("👆 Upload a CSV file to start the analysis.")