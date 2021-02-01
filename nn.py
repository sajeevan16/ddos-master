"""
The design of this comes from here:
http://outlace.com/Reinforcement-Learning-Part-3/
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import RMSprop
from keras.layers.recurrent import LSTM
from keras.callbacks import Callback


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

# nn_params = [[164, 150], [256, 256],
#                      [512, 512], [1000, 1000]]
# nn_param = [128, 128], 

def neural_net(num_sensors, params, load=''):
    model = Sequential()
    
    # First layer.
    model.add(Dense(
        params[0], init='lecun_uniform', input_shape=(num_sensors,)
    ))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    # Second layer.
    model.add(Dense(params[1], init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    # Output layer.
    model.add(Dense(2, init='lecun_uniform'))
    model.add(Activation('sigmoid'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    if load:
        model.load_weights(load)
    print(model.summary())
    return model
