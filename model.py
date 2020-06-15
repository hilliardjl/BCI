from os import listdir
from random import shuffle
import time
import numpy as np
import tensorflow as tf
import pandas as pd

RIGHT_VAL = 0
LEFT_VAL = 1

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
print('Shuffling data...')
labeled_data = []
for ele in right_data:
    labeled_data.append([ele,RIGHT_VAL])
for ele in left_data:
    labeled_data.append([ele,LEFT_VAL])
shuffle(labeled_data)
print('Data shuffled.')
#This step of combining left and right data and then decomposing again is pretty ugly, but its the only way I could figure out to shuffle the stuff.
fft_data = []
labels = []
for ele in labeled_data:
    fft_data.append(ele[0])
    labels.append(ele[1])

train_labels = train.pop('label')
test_labels = test.pop('label')
train_labels = np.asarray(train_labels).reshape((len(train_labels),1))
test_labels = np.asarray(test_labels).reshape((len(test_labels),1))

train = np.reshape(np.asarray(train),(len(train),125,1))
test = np.reshape(np.asarray(test),(len(test),125,1))

print('Data successfully loaded')

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters = 16, kernel_size=3,input_shape = (125,1)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32,activation='relu'),
    tf.keras.layers.Dense(2,activation='softmax')
])
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.fit(x = train,y = train_labels,validation_data = (test,test_labels),epochs=15)

print("Example Prediction: ")
print(model.predict(np.reshape(np.array(range(125)),(1,125,1)))) #wtf...

print("Save model to disk? Y/N")
save_action = str(input())
if save_action.lower()=='y':
    print("Model name?")
    name = input()
    if name == '':
        name = str(time.time())
    model.save('models/saved_model-' + name + '.h5')
    print('Model saved')

