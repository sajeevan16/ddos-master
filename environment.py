
import os

from math import tan, radians, degrees, copysign

import random
import math
import numpy as np


class Environment:
    def __init__(self,Objects=[]):
        # gns3_env.init()

        self.Message = "Welcome"
        self.distance = 0.0
        self.ticks = 60
        self.exit = False
        self.Objects = Objects
        self.returnmenu = False