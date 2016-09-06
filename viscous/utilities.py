import numpy as np

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def scale_lon(lons):
    newlons = lons % 360
    newlons[newlons > 180] -= 360
    return newlons
