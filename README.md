# BCI
This repo is my first shot at using OpenBCI for actual computer control tasks. I started out with the simple goal of classifying a person's thoughts into left versus right, which I thought was going to be much easier than it actually was. Mainly, most of the research that has been done in this field has involved more advanced hardware (16+ channel boards) rather than the 4-channel Ganglion that I had available. Although my results definitely aren't as impressive as those, this was more to prove that the same task could be done somewhat accurately with less advanced hardware. 

# Demo
Check out this [video](https://drive.google.com/file/d/1OuTctT6I4jb8JthzFnYEFEZJ011KdMZ2/view?usp=sharing) for a demo. Because I was thinking right, the box generally moves in that direction!!!

# How it works
At the core of the project is a Tensorflow model trained currently on about 20 minutes total of 0-60 Hz Fast Fourier Transform data. Here's the architecture - 
```
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters = 256, kernel_size=2,input_shape = (4,60),activation='relu'),
    tf.keras.layers.Conv1D(filters=512,kernel_size=2,activation='relu'),
    tf.keras.layers.MaxPooling1D(2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024,activation='relu'),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(2,activation='softmax')
])
```
This model is not really ideal, as typically we would want 2-3 full convolution layers with max pooling as well for good feature extraction. However, I couldn't implement this because I only had a 4 channel board, and both convolutions and max poolings reduce the dimensions of the dataset. One could definitely get better model performance using more convolution layers if possible. 

I used pyLSL to stream the FFT data from the OpenBCI GUI into Python, which is where I did most of the grunt work. See [datacollection.py](https://github.com/hilliardjl/BCI/blob/master/datacollection.py) for my data collection process. Basically, I would input the direction that I was going to be thinking, then visualize a box moving for 20 seconds. This would get saved in the handy .npy format, allowing the numpy array to be read right back into memory for model training. I only saved data up to around 60 Hz, as that's typically the limit for Gamma waves. Maybe play around with this parameter and see if performance improves. 

Once some data is collected, [model.py](https://github.com/hilliardjl/BCI/blob/master/model.py) loads in the numpy arrays saved in the NewFFT folder. The data is shuffled and preprocessed for the model. The data was formatted in 4 vectors of length 60, representing the 4 channels and each of their FFT frequency bins (0-60 Hz). Model output is a softmax array with [0,1] signifying right data and [1,0] representing left data. 

For [game.py](https://github.com/hilliardjl/BCI/blob/master/game.py), the saved model is loaded into memory. This is a pretty simple pygame application - the box moves in a direction if the model is at least 99% confident that the user is thinking in that direction. As shown in the demo, the output is still pretty noisy and inconsistent, but over time, the box tends to move in the direction of thought. 

# Hardware
All that was used for this project was an OpenBCI [Ganglion](https://shop.openbci.com/products/ganglion-board?variant=13461804483) (4-channel) board, EEG paste, electrodes, and the USB dongle. 

Here's my electrode placement:

!(/electrode_placement.jpg)

# Credits
Huge thanks to: 
- Prof. Williams from UVA's ECE department \- he provided the hardware that allowed me to do this project!
- Sentdex ([youtube](https://www.youtube.com/user/sentdex)) After failing to get any results with raw time series data, I was doing some research and found that Sentdex had basically done exactly what I was trying to do using FFT data instead, which is why I switched over. His repo was also a great reference material when I got stuck pulling only 1 channel instead of all 4.  
- Lawhern et. al. ([Paper link](https://arxiv.org/abs/1611.08024)) Although I couldn't use their model architecture due to only having a 4 channel board, this paper gave me the idea to start using convolutions in my network. 
