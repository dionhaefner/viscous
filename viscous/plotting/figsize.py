import viscous

_PAGEWIDTH = 6.90
_TEXTWIDTH = 4.67
_MARGINWIDTH = 1.80
PHI = 1.618

def figsize(n1=1,n2=1,fit="screen"):
    if fit == "screen":
        width = viscous.mpl.rcParams["figure.figsize"][0]
    elif fit == "page":
        width = _PAGEWIDTH
    elif fit == "text":
        width = _TEXTWIDTH
    elif fit == "margin":
        width = _MARGINWIDTH
    else:
        raise ValueError("'fit' must be screen, page, text, or margin")
    return n1*width, n2*width/PHI
