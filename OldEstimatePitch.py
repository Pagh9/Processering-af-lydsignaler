import numpy as np
def estimate_pitch(signal, sample_rate):
    from scipy.signal import correlate

    corr = correlate(signal, signal, mode='full')
    corr = corr[len(corr)//2:]  # behold kun positiv del

    # Ignorer de første ~20 ms (f.eks. 1000 samples) for at undgå DC-offset og støj
    min_lag = int(sample_rate / 1000 * 20)
    peak = np.argmax(corr[min_lag:]) + min_lag

    pitch = sample_rate / peak
    print(f"Estimeret pitch: {pitch:.2f} Hz")
    return pitch