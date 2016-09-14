import matplotlib as mpl
import os
import re

import viscous.read
import viscous.calc
import viscous.utilities
from viscous.plotting import *
from viscous.ipython_tools import *
from viscous.regrid import regrid
from viscous.set_style import set_style

sanitize = sanitize.sanitize
figsize = figsize.figsize
despine = despine.despine
filter_invalid = viscous.utilities.filter_invalid
