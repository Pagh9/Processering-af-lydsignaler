import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import librosa

#load the downloaded guitar sounds

A_major_chord, sr = librosa.load("Downloaded guitar chords/single-acoustic-guitar-hits_69bpm_A_major.wav")
E4_Note, sr = librosa.load("Downloaded guitar chords/guitar-one-chord-string-hit_E_minor.wav")

sd.play(A_major_chord, sr,blocking=True)
#sd.play(E4_Note,blocking=True)

print(f"Total samples: {len(A_major_chord)}")
print(f"Duration in seconds: {len(A_major_chord) / sr:.2f}")

#ploting the C_major_chord as a spectogram
plt.figure(figsize=(10, 4))
plt.specgram(E4_Note, Fs= sr, NFFT=4096, noverlap = 2048, cmap="plasma")
plt.title(f"Spectrogram of real E4 Note")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Intensity (dB)")
plt.tight_layout()
plt.savefig("spectrogram_plot.png")
plt.show()

#plotting C_Major_chord as a waveform
plt.figure(figsize=(10, 4))
plt.plot(A_major_chord)
plt.title("Waveform of Real A major Note")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.savefig("c_major_waveform.png")  # Optional: save it
plt.show()


# using fft and then plots it
def show_fft(signal, sr):
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / sr)
    magnitude = np.abs(fft)

    plt.figure(figsize=(10, 4))
    plt.plot(freqs[:len(freqs)//2], magnitude[:len(magnitude)//2])
    plt.title("Frequency Spectrum of Real E4 Note")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(0, 1000)  # Focus on musical range
    plt.show()

show_fft(E4_Note, sr)

def estimate_pitch(signal, sample_rate):
    from scipy.signal import correlate
    mid = signal[int(len(signal)*0.2):int(len(signal)*0.8)]
    corr = correlate(mid, mid, mode='full')
    corr = corr[len(corr)//2:]

    peak = np.argmax(corr[50:500]) + 50
    pitch = sample_rate / peak
    print(f"Estimated pitch: {pitch:.2f} Hz")
    return pitch

estimate_pitch(E4_Note, sr)