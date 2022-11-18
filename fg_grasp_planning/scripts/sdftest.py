#!/usr/bin/env python3 

import skfmm
import numpy as np 

phi = np.ones((3,3))
phi[1,1] = -1

x = skfmm.distance(phi)

print(x)