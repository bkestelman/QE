import numpy as np

import settings

def sin_func(x, a, b, c, d):
    return a*np.sin(b*x+c)+d
def cos_func(x, a, b, c, d):
    return a*np.cos(np.radians(b*x+c))+d
def cos_sq(x):
    return np.cos(x)*np.cos(x)
def sin_sq(x):
    return np.sin(x)*np.sin(x)
def cos_sq_func(x, a, b, c, d):
    return a*cos_sq(np.radians(b*x+c)) + d

def cos_sq_pvv_manual(x, a):
    return a*cos_sq(np.radians(settings.alpha + x))
def cos_sq_func_pvv_plus(x, a):
    return a*cos_sq(np.radians(settings.alpha - x)) 
def cos_sq_func_pvv_minus(x, a):
    return a*sin_sq(np.radians(settings.alpha + x)) 

def beta_visibility(x, a, b, c, d): # b is V 
    return a/2 * (1 - b*np.sin((x - c)/d))


