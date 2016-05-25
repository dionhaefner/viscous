import numpy as np
from scipy import integrate

def integral(y,x,axis=0):
    y[np.isnan(y)] = 0
    return integrate.simps(y,x,axis=axis)

def average(y,x,axis=0):
    """ Iterates over all axes except 'axis' and averages by slice. Excludes non-finite values"""
    in_arr = np.reshape(np.rollaxis(y,axis,0),(y.shape[axis],-1),order="F").T
    out_arr = np.zeros(in_arr.shape[0])
    for i,s in enumerate(in_arr):
        mask = np.isfinite(s)
        if np.count_nonzero(mask) == 0:
            out_arr[i] = np.nan
            continue
        out_arr[i] = integrate.trapz(s[mask],x[mask])/np.abs(x[mask].max()-x[mask].min())
    return out_arr.reshape(np.delete(y.shape,axis),order="F")

def dydx(y,dx,axis=0):
    return np.gradient(y,dx)[axis]

def ddydxx(y,dx,dx2=None,axis=[0,0]):
    if dx2 is None:
        dx2 = dx
    return dydx(dydx(y,dx,axis=axis[0]),dx2,axis=axis[1])
