import numpy as np
import sounddevice as sd

'''
# exercise 1, making the comb filter
def comb_filter(frequency=110, duration=2.0, sample_rate=44100, decay=0.998):
    delay_samples = int(sample_rate / frequency)
    buffer = np.random.uniform(-1, 1, delay_samples)  # initial pluck noise
    output = np.zeros(int(sample_rate * duration))

    # Use circular buffer for feedback
    for i in range(len(output)):
        output[i] = buffer[i % delay_samples]
        # Feedback with decay
        buffer[i % delay_samples] = decay * output[i]

    return output

# Play it
note = comb_filter(frequency=110, duration=2.0)
sd.play(note, samplerate=44100)
sd.wait()
'''
'''
import numpy as np
import sounddevice as sd

#Exercise 2,
def karplus_strong_lpf(frequency=110, duration=2.0, sample_rate=44100, decay=0.996):
    delay_samples = int(sample_rate / frequency - 0.5)
    buffer = np.random.uniform(-1, 1, delay_samples)
    output = np.zeros(int(sample_rate * duration))

    for i in range(len(output)):
        current = buffer[i % delay_samples]
        next_idx = (i - 1) % delay_samples
        next_sample = buffer[next_idx]

        # Apply simple low-pass filter before feedback
        filtered = 0.5 * (current + next_sample)

        # Store decayed, filtered value back into the buffer
        buffer[i % delay_samples] = decay * filtered

        output[i] = current

    return output

# Play it
note = karplus_strong_lpf(frequency=110, duration=2.0)
sd.play(note, samplerate=44100)
sd.wait()

'''

'''
# Exercise 3
def karplus_strong_excitation(frequency=110, duration=2.0, sample_rate=44100,
                               decay=0.996, excitation_type="noise"):
    delay_samples = int(sample_rate / frequency - 0.5)

    # === Choose Excitation Shape ===
    if excitation_type == "noise":
        buffer = np.random.uniform(-1, 1, delay_samples)
    elif excitation_type == "impulse":
        buffer = np.zeros(delay_samples)
        buffer[0] = 1.0  # single spike at the start
    elif excitation_type == "short_noise":
        buffer = np.zeros(delay_samples)
        burst_len = min(10, delay_samples)
        buffer[:burst_len] = np.random.uniform(-1, 1, burst_len)
    else:
        raise ValueError("Invalid excitation_type. Use 'noise', 'impulse', or 'short_noise'.")

    output = np.zeros(int(sample_rate * duration))

    for i in range(len(output)):
        current = buffer[i % delay_samples]
        next_idx = (i - 1) % delay_samples
        next_sample = buffer[next_idx]

        # Low-pass filter
        filtered = 0.5 * (current + next_sample)
        buffer[i % delay_samples] = decay * filtered
        output[i] = current

    return output

# Try full noise
sd.play(karplus_strong_excitation(frequency=110, excitation_type="noise"), samplerate=44100)
sd.wait()

# Try impulse (pluck at one point)
sd.play(karplus_strong_excitation(frequency=110, excitation_type="impulse"), samplerate=44100)
sd.wait()

# Try short noise burst (like a real pluck)
sd.play(karplus_strong_excitation(frequency=110, excitation_type="short_noise"), samplerate=44100)
sd.wait()
'''

# exercise 5

def karplus_strong_note(frequency=110, duration=2.0, sample_rate=44100,
                        decay=0.996, excitation_type="short_noise"):
    delay_samples = int(sample_rate / frequency - 0.5)

    # Excitation
    if excitation_type == "noise":
        buffer = np.random.uniform(-1, 1, delay_samples)
    elif excitation_type == "impulse":
        buffer = np.zeros(delay_samples)
        buffer[0] = 1.0
    elif excitation_type == "short_noise":
        buffer = np.zeros(delay_samples)
        burst_len = min(10, delay_samples)
        buffer[:burst_len] = np.random.uniform(-1, 1, burst_len)

    output = np.zeros(int(sample_rate * duration))
    for i in range(len(output)):
        current = buffer[i % delay_samples]
        next_sample = buffer[(i - 1) % delay_samples]
        filtered = 0.5 * (current + next_sample)
        buffer[i % delay_samples] = decay * filtered
        output[i] = current
    return output

# 🎸 Define a chord (E minor)
# E2, B2, E3, G3, B3, E4
frequencies = [82.41, 123.47, 164.81, 196.00, 246.94, 329.63]

# Generate each note and sum them
duration = 2.0
sample_rate = 44100
chord = np.zeros(int(sample_rate * duration))

for freq in frequencies:
    note = karplus_strong_note(freq, duration, sample_rate, excitation_type="short_noise")
    chord += note

# Normalize (avoid clipping)
chord /= len(frequencies)

# Play the chord!
sd.play(chord, samplerate=sample_rate)
sd.wait()