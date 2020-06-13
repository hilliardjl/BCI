import pygame as pg
import numpy as np
from pylsl import StreamInlet, resolve_stream
import tensorflow as tf


#PyGame boilerplate setup
pg.init()
pg.display.set_caption('Right vs Left')
screen = pg.display.set_mode((500,500))
clock = pg.time.Clock()
model = tf.keras.models.load_model('models/saved_model-asdf.h5')
print('Model loaded, now establishing connection to LSL stream')
# Establish connection to LSL stream
streams = resolve_stream('type','EEG')
inlet = StreamInlet(streams[0])
#inlet.pull_sample()
print('LSL connection established')

cont = True
box_x = 250
while cont:
    screen.fill((0,0,0))

    #Draw axes
    pg.draw.line(screen,(255,0,0),(250,0),(250,500),3)
    pg.draw.line(screen,(255,0,0),(0,250),(500,250),3)

    pg.draw.rect(screen,(255,255,255),(box_x-10,240,20,20))

    #Prediction
    sample,timestamp = inlet.pull_sample()
    prediction = model.predict(np.array(sample))
    print("Value pulled: " + str(sample))
    print("Prediction: " + str(prediction))

    #Calculates the velocity of the box to be +.01 if prediction = 0 (right think), otherwise -.01 if prediction = 1 (left)
    vel = -.02 * prediction + .01

    #Movement
    delta = clock.tick(30)
    box_x+=delta*vel
    for event in pg.event.get():
        if event.type == pg.QUIT:
            cont = False
    pg.display.update()
