# Signal generation module
# All signals are in the range of [-1,1]
import math

samplingFrequency = 44100
second = samplingFrequency

def sinewave(frequency, n):
    return math.sin(2 * math.pi * frequency * n / samplingFrequency)

def gatewave(frequency, n):
    N = samplingFrequency/frequency
    if n % N < N/2:
        return 1
    return 0

def decay(rate, n):
    return math.e ** -(rate*n/samplingFrequency)

# Converts floating point number to 16-bit signed PCM
def toPCM(value):
    if abs(value) < 0.00001:
        value = 0
    return math.floor((value) * 65535/2).to_bytes(2, byteorder='little', signed=True)
