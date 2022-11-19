#!/usr/bin/env python3 

import skfmm
import numpy as np 

X, Y = np.meshgrid(np.linspace(-1,1,200), np.linspace(-1,1,200))
phi = -1 * np.ones_like(X)
phi[X > -0.5] = 1
phi[np.logical_and(np.abs(Y) < 0.25, X > -0.75)] = 1
d = skfmm.distance(phi, dx=1e-2)