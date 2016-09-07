def vline(x_pos, ax, text="", align="right"):
    ax.axvline(x=x_pos, ymin=0, ymax=1, linestyle="dashed", color="grey") 
    x_bounds = ax.get_xlim()
    ax.annotate(s=text, xy =(.01+((x_pos-x_bounds[0])/(x_bounds[1]-x_bounds[0])),0.01), xycoords='axes fraction', verticalalignment=align, horizontalalignment='right bottom' , rotation = 0)
