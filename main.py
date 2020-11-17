import audio
import signals
import time

audio.start()
f = 500
while True:
    last_t = audio.t
    audio.audioFunction = lambda t: 0.5 * signals.sinewave(f, t) * signals.decay(2, t-last_t)
    f = int(input('Enter frequency: '))

audio.stop()
audio.terminate()
