import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

chords = {
    "E minor": [82.41, 123.47, 164.81, 196.00, 246.94, 329.63],
    "A major": [110.00, 138.59, 164.81, 220.00, 277.18, 329.63],
    "C major": [130.81, 164.81, 196.00, 261.63, 329.63, 392.00],
    "G major": [98.00, 123.47, 147.83, 196.00, 246.94, 392.00],
}

def karplus_strong(frequency=130.81, duration=2.0, sample_rate=44100, decay=0.98, allpass_gain = 0.9):
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
            duration = 4
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


        else:
            print("Invalid choice. Try again.")

play_chord_interface()

# Generate note
note = karplus_strong()

# Play it
sd.play(note, samplerate=44100, blocking=True)

# Plot spectrogram
plt.figure(figsize=(10, 4))
plt.specgram(note, Fs=44100, NFFT=1024, noverlap=512, cmap="plasma")
plt.title("Spectrogram of Karplus-Strong Note")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.ylim(0, 20000)
plt.colorbar(label="Intensity (dB)")
plt.tight_layout()
plt.show()

plt.plot(note[:1000])
plt.title("Waveform (First 1000 samples)")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()