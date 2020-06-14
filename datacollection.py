from pylsl import StreamInlet, resolve_stream
from playsound import playsound
import time
import csv
print("Looking for LSL stream...")

streams = resolve_stream('type','EEG')

inlet = StreamInlet(streams[0])

time_to_collect = 20
samples_to_collect = 100*time_to_collect #Time series data was 200Hz, but FFT appears to be only 100? Not really sure why
print('Input the type of data to be collected, right or left')
direction = input()
print('Data collection beginning in 1 second:')
time.sleep(1)
print('Starting data collection')

data = []
samplesCollected = 0
while samplesCollected<samples_to_collect:
    sample, timestamp = inlet.pull_sample()
    data.append(sample)
    samplesCollected+=1

print("All data collected, beginning write process")
playsound('alert.mp3')

t = time.time()
with open('FFTdata/'+direction+'-'+str(t)+'.csv','w+',newline='') as csvfile:
    writer = csv.writer(csvfile,delimiter=',',)
    for sample in data:
        writer.writerow(sample)
print("Data written")
