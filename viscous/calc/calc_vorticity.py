import numpy as np

def calc_planetary_vorticity(lat,omega=2*np.pi/(24*3600),pi=np.pi):
    return 2*omega*np.sin(np.pi*lat/180)
