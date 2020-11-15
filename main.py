
import signals
import pyaudio
import time
t = 0
p = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, flag):
    global t
    k = b''
    for i in range(frame_count):
        k += signals.toPCM(signals.sinewave(500, i+t) * signals.gatewave(8, i+t))
    t += frame_count
    return (k, pyaudio.paContinue)

stream = p.open(format=8,
                channels=1,
                rate=signals.samplingFrequency,
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(10)
    pass

stream.stop_stream()
stream.close()

p.terminate()

