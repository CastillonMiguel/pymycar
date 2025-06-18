import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


# Parameters for the masses and system geometry

#
#
#     --------------------
#     |                  | 
#     |        ms        | 
#     |                  | 
#     --------------------
#           \       |
#           /      |_|
#           \       |
#        ---------------
#        |             | 
#        |     mu      | 
#        |             | 
#        ---------------
#           \       |
#           /      |_|
#           \       |
#           ---------
#             \   /
#               *      __      __
#       ______________/  \    /  \_________
#                         \__/
#

ms_width  = 0.85
ms_height = 0.3
ms_Z      = 0.9


mu_width  = 0.6
mu_height = 0.2
mu_Z      = 0.3


kw1_length = 0.3
k1_height  = 0.02
cw1_width  = 0.02

d  =  0.05
d0 = -0.1

def add_damper(x, y0, yf, d, text=None):
    line = plt.Line2D((x , x), (y0, yf), color='black', linewidth=2)
    ax.add_line(line)
    
    line0 = plt.Line2D((x-d , x+d), (0.5*(y0+yf), 0.5*(y0+yf)), color='black', linewidth=2)
    ax.add_line(line0)

    line1 = plt.Line2D((x-d , x-d), (0.5*(y0+yf), 0.5*(y0+yf)+0.05), color='black', linewidth=2)
    ax.add_line(line1)

    line2 = plt.Line2D((x+d , x+d), (0.5*(y0+yf), 0.5*(y0+yf)+0.05), color='black', linewidth=2)
    ax.add_line(line2)

    mul = 1.3
    if text is not None:
        ax.text( (x + d)*mul , 0.5*(y0+yf), text, fontsize=16, ha='left')  
    return None

def add_spring(x, y0, yf, d, repetitions, text=None):
    k1_x = np.tile(np.array([  x - d,   x +d ]), repetitions)
    k1_y = np.linspace(y0, yf, len(k1_x))
    ax.plot(k1_x, k1_y, color='black', linewidth=2)
    mul = 1.3
    if text is not None:
        ax.text( ( x - d)*mul , 0.5*(y0+yf), text, fontsize=16, ha='right')  
    return None


with plt.xkcd():

    # Create a new figure
    fig, ax = plt.subplots()

    # Mass -----------------------------------------------------------------------------------------------------------------
    ms = patches.Rectangle((- ms_width / 2, ms_Z), ms_width, ms_height, linewidth=1, edgecolor='black', facecolor='red')
    ax.add_patch(ms)
    ax.text( 0, ms_Z+0.5*ms_height, '$m_s$', fontsize=16, ha='center')  

    mu = patches.Rectangle((- mu_width / 2, mu_Z), mu_width, mu_height, linewidth=1, edgecolor='black', facecolor='blue')
    ax.add_patch(mu)
    ax.text( 0, mu_Z+0.5*mu_height, '$m_u$', fontsize=16, ha='center') 
    
    # Spring -----------------------------------------------------------------------------------------------------------------
    add_spring( -mu_width/4, ms_Z, mu_Z+mu_height, d, 10, "$k$")
    add_spring( -mu_width/4,    0, mu_Z, d, 5, "$k_{w1}$")

    # Damper -----------------------------------------------------------------------------------------------------------------
    add_damper(mu_width / 4, ms_Z, mu_Z+mu_height, d, text="$c_1$")
    add_damper(mu_width / 4,    0, mu_Z, d, text="$c_{w1}$")

    # Bottom triangle
    floorl = plt.Line2D((- mu_width / 2 , 0), (0, d0), color='black', linewidth=2)
    floorr = plt.Line2D((  mu_width / 2 , 0), (0, d0), color='black', linewidth=2)
    floor  = plt.Line2D((- mu_width / 2 ,  mu_width / 2 ), ( 0, 0), color='black', linewidth=2)
    ax.add_line(floorl)
    ax.add_line(floorr)
    ax.add_line(floor)


    
    # Remove x and y ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Set plot limits and aspect ratio
    #ax.set_xlim(- mu_width / 2 *1.25,  mu_width / 2*1.25)
    #ax.set_ylim(0, 2 * spring1_length + 2 * mass1_height)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig('../images/quarter_car3.png')
    plt.show()
