
import os

from math import tan, radians, degrees, copysign
import pygame
import random
import math
import numpy as np
import time
import requests
import datetime
from telnetlib import Telnet
import time
import learning

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
        self.currentState = None
        self.currentStateLabel = 0
        self.currentAction = 0
        self.currentRequest = ""
        self.waiting_packets = []
        self.attacker_pcs = []
        self.legitimate_users = ["192.168.106.78"]
        self.legitimate_users_port =  [5032,5034,5003,5007,5031,5042,5009,5015,5005,5041,5023,5046,5022,5017,5026,5013,5011,5008]
        self.attackers = ["192.168.106.78"]
        self.attackers_port =  [5010]
        self.state_id = 0
        self.statebuffer = [[[0]*learning.NUM_INPUT]*learning.params['window']][0]

    def reset(self, seed=0):
        pass

    def addStateBuffer(self, state):
        self.statebuffer.append(state)
        self.statebuffer.pop(0)

    # def defender_step(self, action):
    #     done = False
    #     info = None
        
    #     return (np.array([state,1,1,1]), np.array([reward]), done, info)
    def get_legitimate(self):
        return self.legitimate_users

    def setState(self,state):
        self.currentState = state
    
    def setStateLabel(self,stateLabel):
        self.currentStateLabel = stateLabel

    def setAction(self,action):
        self.currentAction = action
    
    def setMessage(self,mesg):
        self.message = mesg

    def setStateId(self,id):
        self.state_id = id
    
    def defender_run(self,act,Model):
        dt = self.clock.get_time() / 1000
        self.distance += 1
        SAVE = False
        self.clock.tick(self.ticks)

        ## GET AVAILABILTY LIST
        
        ## State Data
        packet_data = self.statebuffer

        normalized_readings = [[(rx-20.0)/20.0 for rx in y] for y in packet_data]
        # [(rx-20.0)/20.0 for rx in packet_data]
        state = np.array([normalized_readings])
        
        # Calculate the reward
        reward = self.reward_comparison()
        return reward, state, SAVE

    def get_reward(self):
        delay = []
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        reward = 0
        for iport in self.legitimate_users_port:
                try:
                    tn = Telnet('localhost', iport)
                    tn.write("tail -15 result.txt".encode('ascii') + b"\n")
                    output = tn.read_until("#".encode('ascii'), timeout=0.1).decode('ascii').split('\n')
                    
                    for t in output[::-1]:
                        try:
                            if('tail' in t or '#' in t or len(t)<5):
                                continue
                            m,n = t.split()[:2]
                            m,n = float(m),float(n)
                            ts = datetime.datetime.now().timestamp()
                            # print("#######")
                            # print(m,n)
                            # print(ts)
                            # print("#######")
                            if ts - m <1:
                                # print(ts,n,m,"UUUUUUUUUUUUU")
                                delay.append((ts - m, n ))
                                if(0<n<1):
                                    reward += 100*abs(1-(ts-m))*math.exp(-5*n)
                            elif (n==1):
                                reward -= 100*abs(1-(ts-m))
                            else:
                                break
                        except Exception as e:
                            # print(e,"@@@@@@@",t)
                            pass
                    tn.close()
                    # print(delay)
                    #tn.interact()
                except ConnectionRefusedError:
                    print("Error:  ConnectionRefusedError",iport)
                except Exception as e:
                    print("Error ",e,iport)
                finally:
                    # print("****************************")
                    print("reward: ",reward)
                    # print("****************************")
                    if(len(delay)==0):
                        return 0
                    return reward/len(delay)
    
    def reward_comparison(self):
        # Legitimate - 0
        # Attack - 1
        if(int(self.currentStateLabel) == int(self.currentAction)):
            compare_reward = 100
        else:
            compare_reward = -100
        return compare_reward

    def defender_observation_space_dimension(self):
        # Return the dimension of the state
        return self.dimension_of_state

    def defende_action_space_dimension(self):
        # Return the dimension of the action
        return self.dimension_of_action


if __name__ == '__main__':
    environment = Environment()
    while not environment.exit:
        environment.defender_run(1,"S")

