import numpy as np

def calc_planetary_vorticity(lat,omega=np.pi/(24*3600)):
    return 2*omega*np.sin(np.pi*lat/180.)
