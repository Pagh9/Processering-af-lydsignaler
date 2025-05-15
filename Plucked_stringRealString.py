import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import librosa

#load the downloaded guitar sounds
C_major_chord , sr = librosa.load("Downloaded guitar chords/clean-guitar-fusion-one-chord_C_major.wav")
A_major_chord, sr = librosa.load("Downloaded guitar chords/guitar-one-chord-long-bass_78bpm_A_major.wav")
E_minor_chord, sr = librosa.load("Downloaded guitar chords/guitar-one-chord-string-hit_E_minor.wav")

#sd.play(C_major_chord,sr)
sd.play(A_major_chord, sr)
#sd.play(E_minor_chord)

#ploting the C_major_chord as a spectogram
plt.figure(figsize=(10, 4))
plt.specgram(C_major_chord, Fs= sr, NFFT=4096, noverlap = 2048, cmap="plasma")
plt.title(f"Spectrogram of Synthesized Plucked String Chord")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Intensity (dB)")
plt.tight_layout()
plt.savefig("spectrogram_plot.png")
plt.show()

#plotting C_Major_chord as a waveform
plt.figure(figsize=(10, 4))
plt.plot(A_major_chord[:20000])
plt.title("Waveform of Synthesized C Major Chord")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.savefig("c_major_waveform.png")  # Optional: save it
plt.show()


# using fft and then plots it
def show_fft(signal, sample_rate):
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / sample_rate)
    magnitude = np.abs(fft)

    plt.figure(figsize=(10, 4))
    plt.plot(freqs[:len(freqs)//2], magnitude[:len(magnitude)//2])
    plt.title("Frequency Spectrum of Synthesized A Major Chord")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(0, 1000)  # Focus on musical range
    plt.show()

show_fft(A_major_chord, sr)
