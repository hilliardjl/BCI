import pygame as pg
from pylsl import StreamInlet, resolve_stream
import tensorflow as tf


#PyGame boilerplate setup
pg.init()
pg.display.set_caption('Right vs Left')
screen = pg.display.set_mode((300,300))
screen.fill((255,255,255))
# model = tf.keras.models.load_model('models/saved_model-asdf.h5')
# print('Model loaded, now establishing connection to LSL stream')
# #Establish connection to LSL stream
# streams = resolve_stream('type','EEG')
# inlet = StreamInlet(streams[0])
# #inlet.pull_sample()
# print('LSL connection established')

cont = True
box_x = 0
while cont:
    pg.draw.rect(screen,color = (0,0,0),rect = (100,100,100,100))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            cont = False