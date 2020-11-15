# Signal generation module
# Are signals are in the range of [-1,1]
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

def toPCM(value):
    return math.floor((value + 1) * 65535/2).to_bytes(2, byteorder='little')
