import numpy as np
from scipy import interpolate

def isopycnal_mask(target_density,pd):
    """
    Returns a mask in depth-direction along an isopycnal. The target density may be
    given either as an absolute value (in kg/m^3), or as a sigma-value (offset
    from 1000 kg/m^3)
    """
    if target_density < 100:
        target_density += 1000
    pd_nonan = np.copy(pd)
    pd_nonan[~np.isfinite(pd)] = np.inf
    return np.argmin(np.abs(pd_nonan - target_density),axis=0)

def isopycnal_plus(target_density, pd):
    if target_density < 100:
        target_density += 1000
    pd_nonan = np.copy(pd)
    pd_nonan[~np.isfinite(pd)] = np.inf
    diff = pd_nonan - target_density
    diff[diff < 0] = np.inf
    return np.argmin(diff,axis=0)

def isopycnal_minus(target_density, pd):
    if target_density < 100:
        target_density += 1000
    pd_nonan = np.copy(pd)
    pd_nonan[~np.isfinite(pd)] = np.inf
    diff = pd_nonan - target_density
    diff[diff < 0] = np.inf
    return np.argmin(-diff,axis=0)

def isopycnal_arr(arrin,target_density,pd,interp=None):
    """
    Returns the value of an input array along an isopycnal.
    """

    if target_density < 100:
        target_density += 1000

    if not interp:
        i0 = isopycnal_mask(target_density,pd)
        if len(arrin.shape) > 1:
            i1,i2 = np.indices(i0.shape)
            return arrin[i0,i1,i2]
        else:
            return arrin[i0]

    elif interp == "linear":
        i0p = isopycnal_plus(target_density,pd)
	i0m = isopycnal_minus(target_density,pd)
        i0p = np.clip(i0p,0,arrin.shape[0]-1)
        i0m = np.clip(i0m,0,arrin.shape[0]-1)
        i1, i2 = np.indices(i0p.shape)
        x1 = pd[i0p,i1,i2]
        x2 = pd[i0m,i1,i2]
        dx = x2 - x1
        if len(arrin.shape) > 1:
            y1 = arrin[i0p,i1,i2]
            y2 = arrin[i0m,i1,i2]
        else:
            y1 = arrin[i0p]
            y2 = arrin[i0m]
        dy = y2 - y1
	slope = dy/dx
        return y1 + slope * (target_density - x1)

    else:
        raise ValueError("Possible values for interp keyword argument: None, linear")
