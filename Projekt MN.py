# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:40:33 2017

@author: MateuszL_M
"""

import numpy as np
import math as m
from astropy import units as u
from astropy.constants import R_earth

#from matplotlib import ticker
#from matplotlib import pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#plt.ion()
#
#from scipy.integrate import ode
#
#from poliastro.bodies import Earth
#from poliastro.twobody import Orbit
#from poliastro.examples import iss

#from poliastro.twobody.propagation import func_twobody

# Zdefiniowanie punktów na powierzchni Ziemi

# Wołomin   szerkosc =  52°20′24 N, dł↨ugosc = 21°14′31″E
# Nowy York  40°43′N 74°00′W
# Sydney 33°52′S 151°12′E
 
 
R = R_earth/1000 /u.m * u.km
print (R)

P1 = [R, 52, 21]


def convStoC(r): # r = [R,phi,lambda] phi-szerokosc, lamda- długosc
    x = []
    x.append( r[0]*m.cos(r[1]*m.pi/180)*m.cos(r[2]*m.pi/180))
    x.append( r[0]*m.cos(r[1]*m.pi/180)*m.sin(r[2]*m.pi/180))
    x.append( r[0]*m.sin(r[1]*m.pi/180))
    return x*u.km

x = convStoC(P1)
print(x)