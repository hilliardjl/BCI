from os import listdir
from random import shuffle
import time
import numpy as np
import tensorflow as tf
import pandas as pd

RIGHT_VAL = [0,1]
LEFT_VAL = [1,0]
DATA_SPLIT = .9

print("Attempting to load in training data...")

right_data = []
left_data = []

for f in listdir('NewFFT'):
    loaded_file = np.load('NewFFT/' + f)
    print('File ' + str(f) + ' has shape ' + str(loaded_file.shape))
    if 'right' in f:
        for sample in loaded_file:
           right_data.append(sample)
    elif 'left' in f:
        for sample in loaded_file:
            left_data.append(sample)
print('Loaded in ' + str(len(right_data)/10) + ' seconds right data, ' + str(len(left_data)/10) + ' seconds of left data.')

labeled_data = []
for ele in right_data:
    labeled_data.append([ele,RIGHT_VAL])
for ele in left_data:
    labeled_data.append([ele,LEFT_VAL])
shuffle(labeled_data)
#This step of combining left and right data and then decomposing again is pretty ugly, but its the only way I could figure out to shuffle the stuff.

fft_data = []
labels = []
for ele in labeled_data:
    fft_data.append(ele[0])
    labels.append(ele[1])

cutoff = int(len(fft_data)*DATA_SPLIT)
train_data = fft_data[:cutoff]
val_data = fft_data[cutoff:]
train_labels = labels[:cutoff]
val_labels= labels[cutoff:]

train_data = np.asarray(train_data)
val_data = np.asarray(val_data)
train_labels = np.asarray(train_labels)
val_labels = np.asarray(val_labels)

print('Data successfully loaded')

#Ideally there'd be more Conv1D's + MaxPoolings in this network, but I'm limited by the 4 channel board that I have.
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters = 256, kernel_size=2,input_shape = (4,60),activation='relu'),
    tf.keras.layers.Conv1D(filters=512,kernel_size=2,activation='relu'),
    tf.keras.layers.MaxPooling1D(2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024,activation='relu'),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(2,activation='softmax')
])
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
print(model.summary())
history = model.fit(x = train_data,y = train_labels,validation_data = (val_data,val_labels),epochs=9)

print("Example Prediction: ")
print(train_data[0].shape)
print(model.predict(train_data[0].reshape(1,4,60)))

print("Save model to disk? Y/N")
save_action = str(input())
if save_action.lower()=='y':
    print("Model name?")
    name = input()
    if name == '':
        name = str(time.time())
    model.save('models/saved_model-' + name + '.h5')
    print('Model saved')

