# Machine Fault Detection System

A web-based application for detecting machine faults using vibration data analysis with Intrinsic Time-scale Decomposition (ITD) and Boolean logic.

## Features

- Upload vibration data in CSV format
- Perform ITD decomposition to extract signal components
- Calculate statistical features for each component
- Apply Boolean logic for fault detection
- Interactive visualization of original signal and decomposed components
- Download analysis results and plots

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)
3. Upload a CSV file containing vibration data with two columns:
   - Time: Time points
   - Vibration: Vibration amplitude values

## Input Data Format

The input CSV file should have the following format:
```
Time,Vibration
0.0,0.1
0.1,0.15
0.2,0.12
...
```

## Analysis Parameters

- Number of ITD Components: Controls how many components to extract from the signal
- Mean Threshold: Threshold for mean value to detect faults
- Standard Deviation Threshold: Threshold for standard deviation to detect faults

## Output

The application provides:
- Machine condition status (Normal/Warning/Faulty)
- Statistical features for each component
- Interactive plots of the original signal and decomposed components
- Option to download features and plots

## License

MIT License 