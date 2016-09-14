def sanitize(string):
    import viscous
    if viscous.mpl.rcParams["text.usetex"] is True:
        return "\\texttt{{{}}}".format(string.replace("_","\_"))
    else:
        return string
