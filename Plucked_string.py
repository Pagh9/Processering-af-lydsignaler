import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

#Chord dictionary
chords = {
    "E minor": [82.41, 123.47, 164.81, 196.00, 246.94, 329.63],
    "A major": [110.00, 138.59, 164.81, 220.00, 277.18, 329.63],
    "C major": [130.81, 164.81, 196.00, 261.63, 329.63, 392.00],
    "G major": [98.00, 123.47, 147.83, 196.00, 246.94, 392.00],
}


def karplus_strong(frequency=110, duration=2.0, sample_rate=22050, decay=0.996, allpass_gain = 0.5):
    delay = int(sample_rate / frequency)
    buffer = np.random.uniform(-1, 1, delay)
    output = np.zeros(int(duration * sample_rate))

    # all pass filter memory
    prev_input = 0.0
    prev_output = 0.0

    for i in range(len(output)):
        avg = 0.5 * (buffer[0] + buffer[1])

        allpass_out = -allpass_gain * avg + prev_input+ allpass_gain * prev_output
        prev_input = avg
        prev_output = allpass_out

        output[i] = buffer[0]
        buffer = np.append(buffer[1:], decay * allpass_out)

    # Normalize to avoid clipping
    output = output / np.max(np.abs(output) + 1e-9)
    return output

# 🎛 CLI Interface
def play_chord_interface():
    chord_names = list(chords.keys())

    while True:
        print("\nChoose a chord:")
        for i, name in enumerate(chord_names):
            print(f"{i + 1}. {name}")
        print("0. Quit")

        try:
            choice = int(input("Enter number: ")) - 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == -1:
            print("Goodbye!")
            break
        elif 0 <= choice < len(chord_names):
            chord_name = chord_names[choice]
            freqs = chords[chord_name]
            print(f"Playing: {chord_name}")
            duration = 2.0
            sample_rate = 22050
            chord_signal = np.zeros(int(sample_rate * duration))
            for f in freqs:
                chord_signal += karplus_strong(f, duration, sample_rate)
            chord_signal /= len(freqs)  # normalize
            sd.play(chord_signal, samplerate=sample_rate)
            sd.wait()

            # Plot the waveform (first 2000 samples)
            plt.figure(figsize=(10, 4))
            plt.plot(chord_signal[:2000])
            plt.title(f"Waveform of Plucked String {chord_name} Chord")
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("waveform_plot.png")
            plt.show()

            # Plot the spectrogram
            plt.figure(figsize=(10, 4))
            plt.specgram(chord_signal, Fs=sample_rate, NFFT=4096, noverlap=2048, cmap="plasma")
            plt.title(f"Spectrogram of Synthesized Plucked String {chord_name} Chord")
            plt.xlabel("Time (s)")
            plt.ylabel("Frequency (Hz)")
            plt.colorbar(label="Intensity (dB)")
            plt.tight_layout()
            plt.savefig("spectrogram_plot.png")
            plt.show()

            show_fft(chord_signal, sample_rate)

        else:
            print("Invalid choice. Try again.")

sample_rate = 22050
duration = 4.0
frequency = 130  # A2
note = karplus_strong(frequency=frequency, duration=duration, sample_rate= sample_rate)

avg_amplitude = np.mean(np.abs(note))
print(f"Average Amplitude: {avg_amplitude}")


def show_fft(signal, sample_rate):
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / sample_rate)
    magnitude = np.abs(fft)

    plt.figure(figsize=(10, 4))
    plt.plot(freqs[:len(freqs)//2], magnitude[:len(magnitude)//2])
    plt.title("Frequency Spectrum of Synthesized C Major Chord")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)

    plt.tight_layout()
    plt.xlim(0, 1000)  # Focus on musical range
    plt.show()



# ▶ Run it
play_chord_interface()


'''
# Plot the waveform (first 2000 samples)
plt.figure(figsize=(10, 4))
plt.plot(note[:2000])
plt.title(f"Waveform of Plucked String (f = {frequency} Hz) {chord_name} Chord")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.savefig("waveform_plot.png")
plt.show()

# Plot the spectrogram
plt.figure(figsize=(10, 4))
plt.specgram(note, Fs=sample_rate, NFFT=1024, noverlap=512, cmap="plasma")
plt.title(f"Spectrogram of Synthesized Plucked String {chord_name} Chord")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Intensity (dB)")
plt.tight_layout()
plt.savefig("spectrogram_plot.png")
plt.show()
'''
# Save to WAV file
scaled = (note * 32767).astype(np.int16)
write("plucked_string.wav", sample_rate, scaled)
print("Saved waveform_plot.png, spectrogram_plot.png, and plucked_string.wav")


