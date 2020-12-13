
import os

from math import tan, radians, degrees, copysign
import pygame
import random
import math
import numpy as np


class Environment:
    def __init__(self,Objects=[]):
        # gns3_env.init()
        self.message = "Welcome"
        self.distance = 0.0
        self.ticks = 60
        self.clock = pygame.time.Clock()
        self.exit = False
        self.objects = Objects
        self.returnmenu = False
        self.dimension_of_state = 0
        self.dimension_of_action = 0
        self.currentState =0
        self.currentRequest = ""
        self.waiting_packets = []
        self.attacker_pcs = []
        self.legitimate_users = []

    def reset(self, seed=0):
        pass

    # def defender_step(self, action):
    #     done = False
    #     info = None
        
    #     return (np.array([state,1,1,1]), np.array([reward]), done, info)
    
    def setState(self,state):
        self.currentState = state
    
    def defender_run(self,act,Model):
        dt = self.clock.get_time() / 1000
        self.distance += 1
        SAVE = False
        self.clock.tick(self.ticks)
        reward = -1

        ## GET AVAILABILTY LIST 
        

        ## State Data
        packet_data = ""
        normalized_readings = [(rx-20.0)/20.0 for rx in packet_data]
        state = np.array([normalized_readings])

        # Calculate the reward

        return reward, state, SAVE


    def defender_observation_space_dimension(self):
        # Return the dimension of the state
        return self.dimension_of_state

    def defende_action_space_dimension(self):
        # Return the dimension of the action
        return self.dimension_of_action


if __name__ == '__main__':
    game = Environment()
    while not game.exit:
        game.defender_run(1,"S")