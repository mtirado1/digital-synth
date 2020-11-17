import signals
import pyaudio
t = 0
p = pyaudio.PyAudio()

audioFunction = lambda x: 0

yIndex = 0
yPrev = [0] * 10

def callback(in_data, frame_count, time_info, flag):
    global t
    k = b''
    for i in range(frame_count):
        y = audioFunction(i+t)
        yPrev.insert(0, y)
        yPrev.pop()
        k += signals.toPCM(y)
    t += frame_count
    return (k, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(2),
                channels=1,
                rate=signals.samplingFrequency,
                output=True,
                stream_callback=callback)

def start():
    stream.start_stream()


def stop():
    stream.stop_stream()
    stream.close()

def terminate():
    p.terminate()
