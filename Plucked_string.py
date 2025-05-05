import numpy as np
import sounddevice as sd

def karplus_strong(frequency=110, duration=4.0, sample_rate=44100, decay=0.996):
    N = int(sample_rate / frequency)  # Delay line length
    buffer = np.random.uniform(-1, 1, N)  # White noise burst as initial pluck
    output = np.zeros(int(sample_rate * duration))

    for i in range(len(output)):
        output[i] = buffer[0]
        avg = decay * 0.5 * (buffer[0] + buffer[1])  # Simple low-pass filter
        buffer = np.append(buffer[1:], avg)

    return output

# Example: Play a plucked string (A2 = 110 Hz)
sound = karplus_strong(frequency=50, duration=4.0)
sd.play(sound, samplerate=44100)
sd.wait()
