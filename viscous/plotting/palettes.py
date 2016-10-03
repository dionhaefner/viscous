import matplotlib.cm as mplcm
import matplotlib.colors as mplc
import numpy as np

import viscous.plotting.husl as husl

def light(**kwargs):
    light = (.99, .99, .99)
    colors = [light,husl.husl_to_rgb(240,99,55)]
    return mplc.LinearSegmentedColormap.from_list("husl_light",colors)

def dark(**kwargs):
    dark = (.15, .15, .15)
    colors = [dark,husl.husl_to_rgb(240,99,55)]
    return mplc.LinearSegmentedColormap.from_list("husl_dark",colors)

def diverging(**kwargs):
    light = (.99, .99, .99)
    colors = [husl.husl_to_rgb(240,99,55),light,husl.husl_to_rgb(11,99,35)]
    return mplc.LinearSegmentedColormap.from_list("husl_diverging",colors)

def contours(**kwargs):
    length = 40
    hues = np.linspace(0, 360, length + 1)[1:]
    return mplc.ListedColormap([husl.husl_to_rgb(h_i, 90, 65) for h_i in hues],"vcontours")
