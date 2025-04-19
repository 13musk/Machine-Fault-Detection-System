import numpy as np
import matplotlib.pyplot as plt
from itd import itd

# Generate a sample signal (replace with real ITD data later)
x = np.sin(np.linspace(0, 10, 1000)) + np.random.randn(1000) * 0.1

# Apply ITD Decomposition
H = itd(x)

# Plot results

plt.plot(x, label="Original Signal", linewidth=2)
for i, prc in enumerate(H):
    plt.plot(prc, linestyle="--", label=f"PRC {i+1}")
plt.legend()
plt.title("Intrinsic Time-Scale Decomposition (ITD)")
plt.show()

 