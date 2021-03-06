# Signal generation module
# All signals are in the range of [-1,1]
import math
import audio
import random
samplingFrequency = 44100
second = samplingFrequency

# Modules

class Oscillator:
    def __init__(self, function, gain, frequency, enabled):
        self.function = function
        self.gain = gain
        self.frequency = frequency
        self.enabled = False
    def value(self, n):
        if self.enabled:
            return self.gain * self.function(self.frequency, n)
        return 0

class Modulator:
    def __init__(self, mode, function, gain, frequency, enabled):
        self.modulationMode = mode
        self.function = function
        self.frequency = frequency
        self.enabled = False
    def value(self, f, n):
        if self.enabled:
            return self.modulationMode(f, self.function, self.gain, self.frequency, n)
        return f(n)


# Signals

def sinewave(frequency, n):
    return math.sin(2 * math.pi * frequency * n / samplingFrequency)

def sinewaveIntegral(frequency, n):
    return 1 - math.cos(2 * math.pi * frequency * n / samplingFrequency)

def gatewave(frequency, n):
    if frequency == 0:
        return 1
    N = samplingFrequency/frequency
    if n % N < N/2:
        return 1
    return 0

def squarewave(frequency, n):
    if frequency == 0:
        return 1
    N = samplingFrequency/frequency
    if n % N < N/2:
        return 1
    return -1

def triangularwave(frequency, n):
    if frequency == 0:
        return 1
    N = samplingFrequency/frequency
    k = n%N
    if n % N < N/2:
        return 1 + (k*(-2/(N/2)))
    return -1 + ((k-N/2)*(2/(N/2)))

def triangularwaveIntegral(frequency, n):
    if frequency == 0:
        return 0
    N = samplingFrequency/frequency
    k = n%N
    if k < N/2:
        return k - k*k/(N/2)
    return -(k-N/2) + (k - N/2) * (k - N/2) / (N/2)

def rampwave(frequency, n):
    if frequency == 0:
        return 1
    N = samplingFrequency/frequency
    k = n%N
    return 1 + (k*(-2/N))

def rampwaveIntegral(frequency, n):
    if frequency == 0:
        return 1
    N = samplingFrequency/frequency
    k = n%N
    return k + k*k/N

def noisewave(frequency, n):
    return random.random()

def AmplitudeModulation(f1, f2, gain, freq, t):
    return (0.5 + 0.5*gain*f2(freq, t)) * f1(t)

def FrequencyModulation(f1, f2, gain, freq, t):
    if f2 == sinewave:
        return f1(t + samplingFrequency * gain * sinewaveIntegral(freq, t) / 10)
    elif f2 == squarewave:
        return f1(t + samplingFrequency * gain * triangularwave(freq, t) / 10)
    elif f2 == triangularwave:
        return f1(t +  gain * triangularwaveIntegral(freq, t))
    elif f2 == rampwave:
        return f1(t +  gain * rampwaveIntegral(freq, t))

def lowPassFilter(x, gain, f, n):
    # Y(z)/X(z) =  K *   (z+1)*f   /   z + (2f -1)
    # Y(Z) = K * (z+1)*f * X(Z) /  z + (2f-1)
    # Y(z) *(z + (2f-1)) = K (z+1)*f * X(z)
    # Y(z) *(1 + (2f-1)z^(-1) ) = K (1 +z^(-1))*f * X(z)
    # Y(z) = K (1 + z^(-1))*f * X    - (2f-1)z^(-1) Y(z)
    xn = x(n)
    return xn * (1-gain) + gain * f * (xn + x(n-1)) - (2*f-1) * audio.yPrev[0]

def highPassFilter(x, gain, f, n):
    # Y(z)/X(z) =  K * (z-1)*(1-f) / z + (2f -1)
    # Y(Z) = K * (z-1)*(1-f) * X(Z) /  z + (2f-1)
    # Y(z) *(z + (2f-1)) = K (z-1)*(1-f) * X(z)
    # Y(z) *(1 + (2f-1)z^-1) = K (1-z^-1)*(1-f) * X(z)
    # Y(z) = K (X(z)-X(z-1))*(1-f) - (2f-1)Y(z-1)
    xn = x(n)
    return xn * (1 - gain) + gain * (1-f) * (xn - x(n-1)) - (2*f-1) * audio.yPrev[0]


oscillators = {'Sine Wave': sinewave,'Square Wave': squarewave,'Triangular Wave': triangularwave,'Ramp Wave': rampwave,'Noise Wave': noisewave} # Signals generators
modulators = {'Sine Wave': sinewave, 'Square Wave': squarewave, 'Triangular Wave': triangularwave,'Ramp Wave': rampwave} # AM/FM modulators
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
