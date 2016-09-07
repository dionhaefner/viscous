import viscous

def figsize(n1=1,n2=1):
    x, y = viscous.mpl.rcParams["figure.figsize"]
    return x*n1, y*n2
