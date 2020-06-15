from pylsl import StreamInlet, resolve_stream
from time import sleep
print("Looking for stream")
streams = resolve_stream("type",'EEG')

inlet = StreamInlet(streams[0])
lst = []
for i in range(4):
    sample, timestamp = inlet.pull_sample()
    print(str(timestamp) + str(sample))