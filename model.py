from os import listdir
import time
import numpy as np
import tensorflow as tf
import pandas as pd


print("Attempting to load in training data...")
right_frames = []
left_frames = []
for f in listdir('data/'):
    df = pd.read_csv('data/'+f,header = None)
    if 'right' in f:
        right_frames.append(df)
    else:
        left_frames.append(df)
right_data = pd.concat(right_frames)
left_data = pd.concat(left_frames)
print('Found ' + str(right_data.shape[0]/200) + ' seconds of right data, ' + str(left_data.shape[0]/200) + ' seconds of left data.')

right_data['label']=0 #These labels can be changed later, just make sure they're consistent
left_data['label']=1 #Right =0,left=1

overall_data = pd.concat([right_data,left_data])
overall_data = overall_data.reset_index(drop=True)

train= overall_data.sample(frac=.8,random_state=0)
test = overall_data.drop(train.index)
train_labels = train.pop('label')
test_labels = test.pop('label')
print('Data successfully loaded')

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128,activation='relu',input_shape=[4]),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(256,activation='relu'),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(1,activation='sigmoid')
])
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.fit(train,train_labels,validation_data = (test,test_labels),epochs=10)

print("Prediction: ")
print(model.predict(np.reshape(np.array([10,10,10,10]),(1,4)))) #wtf...

print("Save model to disk? Y/N")
save_action = str(input())
if save_action.lower()=='y':
    print("Model name?")
    name = input()
    if name == '':
        name = str(time.time())
    model.save('models/saved_model-' + name + '.h5')
    print('Model saved')

