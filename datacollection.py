from pylsl import StreamInlet, resolve_stream
import numpy as np
from playsound import playsound
import time
import csv
print("Looking for LSL stream...")

streams = resolve_stream('type','EEG')

inlet = StreamInlet(streams[0])

time_to_collect = 20
samples_to_collect = 25*time_to_collect #Time series data was 200Hz, but FFT appears to be only 100. Because we have 4 channels, we reduce the time for a whole measurement down to 25 Hz.
print('Input the type of data to be collected, right or left')
direction = input()
print('Data collection beginning in 1 second:')
time.sleep(1)
print('Starting data collection')

data = []
samplesCollected = 0
while samplesCollected<samples_to_collect:
    sampleData = []
    for i in range(4): # Collect 1 sample of FFT data for each channel
        sample, timestamp = inlet.pull_sample()
        sampleData.append(sample[0:60]) #Only record up to 60 hz, as that's typically the limit for Gamma waves- anything more than that isn't really gonna be useful for what I'm trying to do
    data.append(sampleData)
    samplesCollected+=1

print("All data collected, beginning write process")
playsound('alert.mp3')

data = np.asarray(data)
print(data.shape)

t = time.time()
np.save('NewFFT/' + direction + '-' + str(t) + '.npy',data) #Big thanks to stackoverflow for making me realize there's a file format for storing N-dimensional numpy arrays, savetxt was only for 2d or 1d.
print("Data written")
