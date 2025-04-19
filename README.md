# Machine-Fault-Detection-System
# 🔧 Machine Fault Detection System (In Progress)

A web-based diagnostic tool for rotating machinery using signal decomposition, statistical feature extraction, and Boolean logic to classify machine conditions.

> 🎯 Built using Python and Streamlit, this project aims to provide a lightweight, explainable solution for identifying machine faults based on vibration data.

---

## 🧠 Project Highlights

- ✅ Signal decomposition using **Intrinsic Time-scale Decomposition (ITD)**
- ✅ Feature extraction (Mean, Standard Deviation, RMS, etc.)
- ✅ Boolean logic for fault classification
- ✅ User-friendly **Streamlit app** with:
  - 📈 Time-series plots & signal distribution
  - 🧠 Boolean decision table
  - 🚨 Fault classification as **Normal / Warning / Faulty**
  - 📥 CSV & plot downloads

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (for the web UI)
- **NumPy / Pandas** (for data processing)
- **Plotly** (for signal visualization)
- **Matplotlib / Seaborn** (optional analysis tools)

---

## ⚙️ How It Works (Flow)

```mermaid
graph TD;
    A[Upload Vibration CSV] --> B[Apply ITD Decomposition];
    B --> C[Extract PRC Components];
    C --> D[Calculate Features];
    D --> E[Apply Boolean Rules];
    E --> F[Classify: Normal / Warning / Faulty];
    F --> G[Display Results + Plots];
    G --> H[Allow CSV/HTML Downloads];
