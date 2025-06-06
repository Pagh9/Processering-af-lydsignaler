import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

#Chord dictionary
chords = {
    "E4": [329.63],
    "A Major": [110, 138.6, 164.8],
    "G String": [196.00],
}

def karplus_strong(frequency=110, duration=2.0, sample_rate=22050, decay=0.998,
                   lp_coeff=0.5):
    # Compute ideal (fractional) delay
    ideal_delay = sample_rate / frequency
    int_delay = int(np.floor(ideal_delay - 0.5))
    fractional_part = ideal_delay - int_delay - 0.5

    # Allpass coefficient for fractional delay
    b = (1 - fractional_part) / (1 + fractional_part)

    # Initial buffer: noise burst shaped by Hanning window
    buffer = np.random.uniform(-1, 1, int_delay)
    buffer *= np.hanning(len(buffer))

    output_len = int(sample_rate * duration)
    output = np.zeros(output_len)

    # Filter states
    prev_lp_out = 0.0
    ap_x1, ap_y1 = 0.0, 0.0  # allpass previous input/output

    for n in range(output_len):
        current = buffer[n % int_delay]

        # --- 1. IIR Low-pass filter ---
        lp_out = (1 - lp_coeff) * current + lp_coeff * prev_lp_out
        prev_lp_out = lp_out

        # --- 2. Allpass filter for fractional delay ---
        ap_out = b * lp_out + ap_x1 - b * ap_y1
        ap_x1 = lp_out
        ap_y1 = ap_out

        # Output and feedback
        output[n] = ap_out
        buffer[n % int_delay] = decay * ap_out

    # Normalize
    output = output / (np.max(np.abs(output)) + 1e-9)
    return output


# 🎛 CLI Interface
def play_chord_interface(sample_rate=22050, duration = 2.0):
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
            chord_signal = np.zeros(int(sample_rate * duration))
            for f in freqs:
                #sd.play(karplus_strong(f, duration, sample_rate), sample_rate, blocking=True)
                chord_signal += karplus_strong(f, duration, sample_rate)
            chord_signal /= len(freqs)  # normalize
            sd.play(chord_signal, samplerate=sample_rate)
            print(f"DEBUG: You selected index {choice}, which is {chord_name}")
            print("DEBUG: Frequencies in chord:", freqs)
            sd.wait()

            # Plot the waveform (first 2000 samples)
            plt.figure(figsize=(10, 4))
            plt.plot(chord_signal[:2000])
            plt.title(f"Waveform of Synthesized {chord_name} Note")
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("waveform_plot.png")
            plt.show()

            # Plot the spectrogram
            plt.figure(figsize=(10, 4))
            plt.specgram(chord_signal, Fs=sample_rate, NFFT=4096, noverlap=2048, cmap="plasma")
            plt.title(f"Spectrogram of Synthesized Plucked {chord_name} Note")
            plt.xlabel("Time (s)")
            plt.ylabel("Frequency (Hz)")
            plt.colorbar(label="Intensity (dB)")
            plt.tight_layout()
            plt.savefig("spectrogram_plot.png")
            plt.show()

            show_fft(chord_signal, sample_rate)

        else:
            print("Invalid choice. Try again.")






def show_fft(signal, sample_rate):
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / sample_rate)
    magnitude = np.abs(fft)

    plt.figure(figsize=(10, 4))
    plt.plot(freqs[:len(freqs)//2], magnitude[:len(magnitude)//2])
    plt.title("Frequency Spectrum of Synthesized E4 Note Chord")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)

    plt.tight_layout()
    plt.xlim(0, 1000)  # Focus on musical range
    plt.show()



# ▶ Run it
play_chord_interface()

sample_rate = 22050

note = karplus_strong()

sd.play(note, sample_rate)
