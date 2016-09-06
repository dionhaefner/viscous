import seaborn as sns
import os
import copy
import math

import viscous.read
import viscous.calc
import viscous.utilities
from viscous.plotting import *
from viscous.ipython_tools import *
from viscous.regrid import regrid

sanitize = sanitize.sanitize
figsize = figsize.figsize
subplots = subplots.subplots
despine = sns.despine

def set_style(out_type="screen"):
    sns.mpl.rcdefaults()
    golden_ratio = (math.sqrt(5) - 1)/2
    screen_width = 10.
    paper_width = 6.9
    if out_type == "screen":
        # produce screen-optimized plots
        rc_params = {
                     "figure.figsize": (screen_width,screen_width*golden_ratio),
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
        context = "notebook"
    elif out_type == "pdf":
        # assume we are producing printing quality plots
        rc_params = {
                 "backend": "ps",
                 "ps.papersize": "A4",
                 "figure.figsize": (paper_width,paper_width*golden_ratio),
                 "figure.titlesize": 11,
                 "axes.titlesize": 10,
                 "font.size": 10,
                 "text.color": "black",
                 "savefig.bbox": "standard",
                 "savefig.format": "pdf",
                 "savefig.dpi": 300,
                 "font.family": "serif",
                 "font.serif": "Linux Libertine O",
                 "font.sans-serif": "Fira Sans",
                 "text.usetex": True,
                 "text.latex.preamble": [
					 "\\usepackage[T1]{fontenc}",
					 "\\usepackage[utf8]{inputenc}",
					 "\\usepackage{amsmath}",
					 "\\usepackage{libertine}",
                     "\\usepackage{FiraSans}",
                     "\\usepackage{newtxmath}",
                     "\\usepackage{FiraMono}",
                     "\\usepackage{siunitx}"
                    ]
                 }
        font_scale = 1.
        context = "notebook"
    elif out_type == "pgf":
        # create pgf file for inclusion with pdflatex
        rc_params = {
                 "backend": "pgf",
                 "figure.figsize": (paper_width,paper_width*golden_ratio),
                 "figure.titlesize": 11,
                 "axes.titlesize": 10,
                 "axes.labelsize": 9,
                 "axes.facecolor": "white",
                 "font.size": 10,
                 "text.color": "black",
                 "savefig.bbox": "standard",
                 "savefig.format": "pgf",
                 "savefig.dpi": 300,
                 "font.family": "serif",
                 "font.serif": [],
                 "font.sans-serif": [],
                 "text.usetex": True,
                 "pgf.texsystem": "pdflatex",
                 "pgf.preamble": [
					 "\\usepackage[T1]{fontenc}",
					 "\\usepackage[utf8]{inputenc}",
					 "\\usepackage{amsmath}",
					 "\\usepackage{libertine}",
                     "\\usepackage{FiraSans}",
                     "\\usepackage{newtxmath}",
                     "\\usepackage{FiraMono}",
                     "\\usepackage{siunitx}"
                    ]
                 }
        font_scale = 1.
        context = "notebook"
    else:
        raise ValueError("Unrecognized output type: " + str(out_type))

    sns.set(style="ticks", context=context, color_codes=True, font_scale=font_scale, rc=rc_params)
    sns.mpl.pyplot.close()
