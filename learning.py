
import numpy as np
import random
import csv
from nn import neural_net, LossHistory
import os.path
import timeit

NUM_INPUT = 2
GAMMA = 0.9 # Forgetting.
TUNING = False  # If False, just use arbitrary, pre-selected params.

def train_net(model, params, environment, modelname="untitle", train_frames = 50000):
    filename = modelname#params_to_filename(params)
    observe = 1000  # Number of frames to observe before training.
    epsilon = 1
    train_frames = train_frames  # Number of frames to play.
    batchSize = params['batchSize']
    buffer = params['buffer']
