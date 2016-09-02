from seaborn import light_palette, dark_palette, diverging_palette, color_palette

def light(**kwargs):
    return light_palette((210, 90, 60), input="husl", **kwargs)

def dark(**kwargs):
    return dark_palette((210, 90, 60), input="husl", **kwargs)

def diverging(**kwargs):
    return diverging_palette(220, 20, **kwargs)

def contour(length=10, **kwargs):
    try:
        length = len(length)
    except TypeError:
        pass
    return color_palette("husl", length, **kwargs)
