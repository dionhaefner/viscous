import re
import os

from viscous import mpl

STYLE_PATH = os.path.join(os.path.dirname(__file__), "plotting/styles/")
STYLE_NAME = "v{}.mplstyle"

_DEFAULT_RC = None

def set_style(*styles):
    if not hasattr(styles, '__iter__'):
        styles = (styles,)
    available_styles = [re.match(STYLE_NAME.format("(\\w+)"),x).group(1) for x in os.listdir(STYLE_PATH)]
    style_paths = [STYLE_PATH + STYLE_NAME.format("default")]
    for style in styles:
        if style in available_styles:
             style_paths.append(STYLE_PATH + STYLE_NAME.format(style))
        else:
             raise ValueError("Style {} not found. Available styles: {}".format(style,", ".join(available_styles)))
    global _DEFAULT_RC
    if _DEFAULT_RC is None:
        _DEFAULT_RC = dict(mpl.rcParams)
    mpl.rcParams.update(_DEFAULT_RC)
    mpl.style.use(style_paths)
