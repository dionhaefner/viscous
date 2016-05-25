import seaborn as sns
import os
import copy
import math

_usetex = False

import viscous.read
import viscous.calc
import viscous.utilities
from viscous.plotting import *
from viscous.ipython_tools import *

sanitize = sanitize.sanitize
figsize = figsize.figsize
subplots = subplots.subplots

def set_style(usetex=False):
    global _usetex
    _usetex = usetex
    
    sns.mpl.rcdefaults()
    golden_ratio = (1 + math.sqrt(5))/2
    screen_width = 10.
    paper_width = 4.786
    if usetex: # assume we are producing printing quality plots
        rc_params = {
                 "figure.figsize": (paper_width,paper_width/golden_ratio),
                 "figure.dpi": 800/paper_width,
                 "figure.titlesize": 12,
                 "savefig.dpi": 300,
                 "savefig.bbox": "standard",
                 "savefig.format": "pdf",
                 "font.family": "sans-serif",
                 "font.serif": "Linux Libertine O",
                 "font.sans-serif": "Fira Sans",
                 "text.usetex": True,
                 "text.latex.preamble": ["\\usepackage{gensymb}",
                                         "\\usepackage{FiraSans}",
                                         "\\usepackage{mathpazo}",
                                         "\\usepackage{FiraMono}",
                                         "\\usepackage[T1]{fontenc}"]
                 }
        font_scale = .5
    else: # produce screen-optimized plots
        rc_params = {
                     "figure.figsize": (screen_width,screen_width/golden_ratio),
                     "figure.dpi": 800/screen_width,
                     "figure.titlesize": 24,
                     "savefig.dpi": 2*800/screen_width,
                     "savefig.bbox": "tight",
                     "savefig.format": "png",
                     "font.family": "sans-serif",
                     "font.serif": "Linux Libertine O",
                     "font.sans-serif": "Bitstream Vera Sans",
                     "lines.antialiased": True
                     }
        font_scale = 1.

    sns.set(style="dark", context="notebook", font_scale=font_scale, rc=rc_params)
    sns.mpl.pyplot.close()
