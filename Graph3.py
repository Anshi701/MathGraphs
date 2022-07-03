import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


xA = 0
xB = 5
tA = 0
tB = 1
Xdata, h    = np.linspace(xA, xB, 400, retstep=True)
T    , r    = np.linspace(tA, tB, 400, retstep=True)



fig, (ax1, ax2) = plt.subplots(2,1)
Ydata = [[], []]
line1, = ax1.plot([], [], lw=2, label='Аналитическое решение')
line2, = ax2.plot([], [], lw=2, color='r', label='Численное решение')
ax1.legend()
ax2.legend()
line = [line1, line2]

#######################

U_func = lambda x, t: 1 + math.cos(3*math.pi*x)*math.cos(3*math.pi*t) + math.sin(2*math.pi*t)*math.cos(2*math.pi*x)/(2*math.pi)

ratio = (r/h)**2

U_jn1 = lambda U_1jn, U_jn, U_j1n, U_1nj:   ratio * U_1jn + 2 * (1  - ratio)  *  U_jn + ratio * U_j1n - U_1nj
f_x = lambda x: 1 + math.cos(3 * math.pi * x)
g_x = lambda x:     math.cos(2 * math.pi * x)

#######################

def init():
    box = 3
    for ax in [ax1, ax2]:
        ax.set_xlim(xA, xB)   
        ax.set_ylim(-1, box)

    ####  инициализация численного решения ####
    layer0 = []
    layer1 = []
    for x in Xdata:
        
        layer0.append(f_x(x))
        layer1.append(f_x(x) + r * g_x(x))

    Ydata[1].append(layer0)
    Ydata[1].append(layer1)
    ###########################################
    
    return line 

def update(frame):
    
    Ydata[0] = []
    for x in Xdata:
        Ydata[0].append(   U_func(x, frame)  )
    

    layer = []
    j = 0
    end = len(Ydata[1][-1]) - 1
    for x in Xdata:
        if j == 0:   
            layer.append(  U_jn1(   Ydata[1][-1][j  ], Ydata[1][-1][j], Ydata[1][-1][j+1], Ydata[1][-2][j]  )  ) # j-1 = j
        elif j == end: 
            layer.append(  U_jn1(   Ydata[1][-1][j-1], Ydata[1][-1][j], Ydata[1][-1][j  ], Ydata[1][-2][j]  )  ) # j+1 = j
        else: layer.append(  U_jn1(   Ydata[1][-1][j-1], Ydata[1][-1][j], Ydata[1][-1][j+1], Ydata[1][-2][j]  )  )
        j += 1
    
    Ydata[1].append(layer)

    line[0].set_data(Xdata, Ydata[0])
    line[1].set_data(Xdata, Ydata[1][-3])
    return line

ani = FuncAnimation(fig, update, frames=T,
                    init_func=init, blit=True, interval=30)
plt.show()
