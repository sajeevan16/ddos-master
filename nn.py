"""
The design of this comes from here:
http://outlace.com/Reinforcement-Learning-Part-3/
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import RMSprop
from keras.layers.recurrent import LSTM
from keras.callbacks import Callback

from keras.layers import Bidirectional


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

NUM_INPUT = 23
nn_param = [64, 128,128,128]
params = {
    "batchSize": 64,
    "buffer": 50000,
    "window": 100,
    "nn": nn_param
    }

def neural_net(num_features, window, params, load=''):
    model = Sequential()
    

    # First layer.
    model.add(Bidirectional(LSTM(params[0], activation='tanh', kernel_regularizer='l2', return_sequences=False),input_shape=(window, num_features)))


    # hidden layer.
    model.add(Dense(params[1], init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(params[2], init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(params[3], init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    # Output layer.
    model.add(Dense(2, init='lecun_uniform')) 
    model.add(Activation('sigmoid'))

    rms = RMSprop()
   
    model.compile(loss='mse', optimizer=rms)
    # model.build((window, num_features)) 
    if load:
        model.load_weights(load)
    print(model.summary())
    return model
