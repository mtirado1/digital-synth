# Signal generation module
# All signals are in the range of [-1,1]
import math
import audio
samplingFrequency = 44100
second = samplingFrequency


def sinewave(frequency, n):
    return math.sin(2 * math.pi * frequency * n / samplingFrequency)

def gatewave(frequency, n):
    if frequency == 0:
        return 1
    N = samplingFrequency/frequency
    if n % N < N/2:
        return 1
    return 0

def AmplitudeModulation(f1, f2, gain, freq, t):
    return (1 - abs(gain*f2(freq, t))) * f1(t)

def FrequencyModulation(f1, f2, gain, freq, t):
    if f2 == sinewave:
        return f1(t + samplingFrequency * gain * f2(freq, t)/ 2 / math.pi)
    else:
        return f1(t * (1 + gain * f2(freq, t)))


oscillators = {'Sine Wave': sinewave} # Signals generators
modulators = {'Sine Wave': sinewave, 'Gate Wave': gatewave} # AM/FM modulators
modulationModes = {'AM': AmplitudeModulation, 'FM': FrequencyModulation}

def attack(period, n):
    v = n/period
    if v > 1:
        return 1
    return v

def decay(rate, n):
    return math.e ** -(rate*n/samplingFrequency)

# Converts floating point number to 16-bit signed PCM
def toPCM(value):
    if abs(value) < 0.00001:
        value = 0
    return math.floor((value) * 65535/2).to_bytes(2, byteorder='little', signed=True)
