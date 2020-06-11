import tensorflow as tf
import numpy as np

print("Attempting to load in training data...")
#Training data...


print("Building model")

model = tf.keras.models.Sqeuential([
    tf.keras.layers.
])







# #This model architecure is taken from https://arxiv.org/pdf/1611.08024.pdf
# #I trust that they're much smarter than I am in determining architecture.
#
# #Setting up constants:
# nb_classes = 2
# Chans = ???
# Samples = ???
# dropoutRate = 0.2
# kernLength = 32
# F1 = 8 #Temporal filter count
# F2 =
# #TODO: fix model input shape
#     block1 = tf.keras.layers.Conv2D(F1, (1, kernLength), padding='same',
#                     input_shape=(1, Chans, Samples),
#                     use_bias=False)(input1)
#     block1 = tf.keras.layers.BatchNormalization(axis=1)(block1)
#     block1 = tf.keras.layers.DepthwiseConv2D((Chans, 1), use_bias=False,
#                          depth_multiplier=D,
#                          depthwise_constraint=max_norm(1.))(block1)
#     block1 = tf.keras.layers.BatchNormalization(axis=1)(block1)
#     block1 = tf.keras.layers.Activation('elu')(block1)
#     block1 = tf.keras.layers.AveragePooling2D((1, 4))(block1)
#     block1 = tf.keras.layers.dropoutType(dropoutRate)(block1)
#
#     block2 = tf.keras.layers.SeparableConv2D(F2, (1, 16),
#                          use_bias=False, padding='same')(block1)
#     block2 = tf.keras.layers.BatchNormalization(axis=1)(block2)
#     block2 = tf.keras.layers.Activation('elu')(block2)
#     block2 = tf.keras.layers.AveragePooling2D((1, 8))(block2)
#     block2 = tf.keras.layers.dropoutType(dropoutRate)(block2)
#
#     flatten = tf.keras.layers.Flatten(name='flatten')(block2)
#
#     dense = tf.keras.layers.Dense(nb_classes, name='dense',
#               kernel_constraint=max_norm(norm_rate))(flatten)
