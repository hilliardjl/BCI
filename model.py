from os import listdir
import time
import numpy as np
import tensorflow as tf
import pandas as pd


print("Attempting to load in training data...")
right_frames = []
left_frames = []
for f in listdir('FFTdata/'):
    df = pd.read_csv('FFTdata/'+f,header = None)
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

train= overall_data.sample(frac=.9,random_state=0)
test = overall_data.drop(train.index)
train_labels = train.pop('label')
test_labels = test.pop('label')
train = np.reshape(np.asarray(train),(len(train),125,1))
test = np.reshape(np.asarray(test),(len(test),125,1))
print(train)
print(train.shape)
print('Data successfully loaded')

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters = 16, kernel_size=3,input_shape = (125,1)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32,activation='relu'),
    tf.keras.layers.Dense(1,activation='sigmoid')
])
print(model.summary())
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.fit(train,train_labels,validation_data = (test,test_labels),epochs=1)

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

