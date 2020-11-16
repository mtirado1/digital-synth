import audio
import signals
import time

audio.audioFunction = lambda t: 0.2 * signals.sinewave(500, t) * signals.sinewave(2, t)
audio.start()

while audio.stream.is_active():
    time.sleep(10)
    pass

audio.stop()
audio.terminate()
