def despine(ax):
    ax.spines["top"].set_visible(False)
    ax.xaxis.set_tick_params(top='off')
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_tick_params(right='off')
