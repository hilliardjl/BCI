import pygame as pg
import time
import numpy as np
from pylsl import StreamInlet, resolve_stream
import tensorflow as tf

CONFIDENCE_LEVEL = .65

#PyGame boilerplate setup
pg.init()
pg.display.set_caption('Right vs Left')
HEIGHT = 500
WIDTH = 500
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
model = tf.keras.models.load_model('models/saved_model-fft.h5')
print('Model loaded, now establishing connection to LSL stream')
# Establish connection to LSL stream
streams = resolve_stream('type','EEG')
inlet = StreamInlet(streams[0])
#inlet.pull_sample()
print('LSL connection established')

cont = True
box_x = (WIDTH/2)
time.sleep(2)
while cont:
    screen.fill((0,0,0))

    #Draw axes
    pg.draw.line(screen,(255,0,0),(WIDTH/2,0),(WIDTH/2,HEIGHT),3)
    pg.draw.line(screen,(255,0,0),(0,HEIGHT/2),(WIDTH,HEIGHT/2),3)

    pg.draw.rect(screen,(255,255,255),(box_x-10,(HEIGHT/2)-10,20,20))

    #Prediction
    sample_list = []
    for i in range(4):
        sample,timestamp = inlet.pull_sample()
        sample_list.append(sample[:60])
        print(sample)
    prediction = model.predict(np.asarray(sample_list).reshape(1,4,60))
    print("Value pulled: " + str(sample_list))
    print("Prediction: " + str(prediction))

    #Calculates the velocity of the box to be +.01 if prediction = 0 (right think), otherwise -.01 if prediction = 1 (left)
    if prediction[0][0] > CONFIDENCE_LEVEL:
        box_x-=delta*.01
    elif prediction[0][1] > CONFIDENCE_LEVEL:
        box_x+=delta*.01

    #Force FPS to be at 30, I'm worried about the game running to fast for predictions to take effect.
    delta = clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            cont = False
    pg.display.update()
