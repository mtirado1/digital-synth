import audio
import signals
import time

audio.audioFunction = lambda t: 0.2 * signals.sinewave(500, t) * signals.sinewave(2, t)
audio.start()

input('Press enter to exit.')

audio.stop()
audio.terminate()
