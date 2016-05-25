def sanitize(string):
    import viscous
    if viscous._usetex:
        return "\\verb+" + string + "+"
    else:
        return string
