from scipy import ndimage
import numpy as np
from copy import deepcopy

def calc_noise(v):
    vel0 = deepcopy(v)
    vel0 = np.ma.masked_outside(vel0,-1E10,1E10)
    vel0[vel0.mask] = 0
    vel = np.zeros_like(vel0[0,:,:,:])
    vel_smooth = np.zeros_like(vel0[0,:,:,:])
    for i in range(vel.shape[0]):
        vel[i,:,:] = vel0[0,i,:,:]
        k = np.array([[0, 0, 0],
                    [.25, .5, .25],
                    [0, 0, 0]])
        vel_smooth[i,:,:] = ndimage.convolve(vel[i,:,:], k, mode='constant', cval=0.0)
    v_noise = np.abs(vel_smooth - vel)
    v_noise_avg = np.mean(v_noise,0)
    v_noise_zonalavg = np.mean(v_noise_avg,1)
    return v_noise_zonalavg


