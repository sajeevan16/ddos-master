
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
        self.currentState = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.currentRequest = ""
        self.waiting_packets = []
        self.attacker_pcs = []
        self.legitimate_users = ["192.168.106.78"]
        self.legitimate_users_port =  [5032]

    def reset(self, seed=0):
        pass

    # def defender_step(self, action):
    #     done = False
    #     info = None
        
    #     return (np.array([state,1,1,1]), np.array([reward]), done, info)
    def get_legitimate(self):
        return self.legitimate_users

    def setState(self,state):
        self.currentState = state
    
    def setMessage(self,message):
        self.message = message
    
    def defender_run(self,act,Model):
        dt = self.clock.get_time() / 1000
        self.distance += 1
        SAVE = False
        self.clock.tick(self.ticks)
        reward = 10

        ## GET AVAILABILTY LIST
        
        ## State Data
        packet_data = self.currentState
        normalized_readings = [(rx-20.0)/20.0 for rx in packet_data]
        state = np.array([normalized_readings])
        
        # Calculate the reward
        reward = self.get_reward()
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
                                    reward+= 100*abs(1-(ts-m))*math.exp(-5*n)
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
            

    def defender_observation_space_dimension(self):
        # Return the dimension of the state
        return self.dimension_of_state

    def defende_action_space_dimension(self):
        # Return the dimension of the action
        return self.dimension_of_action


if __name__ == '__main__':
    environment = Environment()
    while not game.exit:
        environment.defender_run(1,"S")

