
import os

from math import tan, radians, degrees, copysign

import random
import math
import numpy as np


class Environment:
    def __init__(self,Objects=[]):
        # gns3_env.init()
        self.message = "Welcome"
        self.distance = 0.0
        self.ticks = 60
        self.exit = False
        self.objects = Objects
        self.returnmenu = False
        self.dimension_of_state = 0
        self.dimension_of_action = 0
        self.attacker = {
            'distributed_pcs' : [],

        }

    def reset(self, seed=0):
        pass

    def defender_step(self, action):
        done = False
        info = None
        
        return (np.array([state,1,1,1]), np.array([reward]), done, info)

    def defender_observation_space_dimension(self):
        # Return the dimension of the state
        return self.dimension_of_state

    def defende_action_space_dimension(self):
        # Return the dimension of the action
        return self.dimension_of_action