def calc_hor_friction(A,B,uxx,uyy,vxx,vyy):
    return A*uxx + B*uyy, A*vyy + B*vxx
    

