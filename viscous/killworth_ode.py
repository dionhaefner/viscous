from scipy.integrate import ode
import numpy as np
import matplotlib.pyplot as plt

y_1 = 4
dy = 0.01
Y = -.96
yf = 2.06   
y_0 = -5

h0 = 1
h0p = 0
def odefun(y,Y0):
    y0, y0p = Y0
    y0pp = -1/h0 * (h0p*y0p + 1/8 * y*(y**2 - y0**2))
    return [y0p,y0pp]

for s in np.linspace(1.0 - 1E-10,1.0,100):
    y0_0 = [y_0, s]
    r = ode(odefun).set_integrator('dopri5',atol=1E-12,rtol=1E-12)
    r.set_initial_value(y0_0,y_0)

    sol = np.empty((0,3))
    sol_vec = [-1000,1]
    while r.successful() and r.t < y_1 and r.y[1] > 0:
        sol_vec = r.integrate(r.t+dy)
        sol_row = np.append(r.t,sol_vec)
        sol = np.vstack((sol,sol_row))
    
    plt.plot(sol[:,0],sol[:,2])
plt.show()
