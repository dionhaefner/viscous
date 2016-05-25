from viscous.plotting.figsize import figsize

import math
import matplotlib.pyplot as plt

def subplots(nrows,ncols,**kwargs):
    return plt.subplots(nrows, ncols, figsize=figsize(1, nrows/(.75 + 0.25*ncols)))

