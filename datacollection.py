from pylsl import StreamInlet, resolve_stream
import time
print("Looking for LSL stream...")

streams = resolve_stream('type','EEG')

inlet = StreamInlet(streams[0])

time_to_collect = 1
samples_to_collect = 200*time_to_collect #Assuming 200 Hz
print('Input the type of data to be collected, right or left')
direction = input()
print('Data collection beginning in 1 second:')

data = []
samplesCollected = 0
while samplesCollected<samples_to_collect:
    sample, timestamp = inlet.pull_sample()
    data.append(sample)
    samplesCollected+=1

print("All data collected, beginning write process")

t = time.time()
f = open('data/'+direction + '-' + str(t) + '.txt','w+')
for sample in data:
    f.write(str(sample) + '\n')
print("Data written")

