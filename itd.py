import numpy as np
from scipy.signal import find_peaks

def itd(x, N_max=10):
    """
    Python implementation of Intrinsic Time-Scale Decomposition (ITD).
    :param x: 1D numpy array (input signal)
    :param N_max: Maximum number of iterations
    :return: H (2D array of PRCs), residual signal
    """
    H = []
    xx = x.flatten()
    E_x = np.sum(x ** 2)
    counter = 0

    while True:
        counter += 1
        L1, H1 = itd_baseline_extract(xx)
        H.append(H1)

        if stop_iter(xx, counter, N_max, E_x):
            H.append(L1)
            break

        xx = L1  # Update for next iteration

    return np.array(H)

def stop_iter(xx, counter, N_max, E_x):
    """
    Determines whether to stop the ITD iterations.
    """
    if counter > N_max:
        return True

    Exx = np.sum(xx ** 2)
    if Exx <= 0.01 * E_x:
        return True

    pks1, _ = find_peaks(xx)
    pks2, _ = find_peaks(-xx)
    pks = np.union1d(pks1, pks2)

    return len(pks) <= 7

def itd_baseline_extract(x):
    """
    Extracts the baseline (L) and high-frequency components (H) from the signal.
    """
    x = x.flatten()
    t = np.arange(len(x))

    alpha = 0.32  

    
    idx_max, _ = find_peaks(x)
    idx_min, _ = find_peaks(-x)
    val_max = x[idx_max]
    val_min = -x[idx_min]

    max_line = np.interp(t, idx_max, val_max)
    min_line = np.interp(t, idx_min, val_min)


    L = alpha * max_line + (1 - alpha) * min_line
    H = x - L  

    return L, H     

 

  