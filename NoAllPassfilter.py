import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

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