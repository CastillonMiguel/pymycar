import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


# Parameters for the masses and system geometry

#
#
#     --------------------
#     |                  | 
#     |        m         | 
#     |                  | 
#     --------------------
#           \       |
#           /      |_|
#           \       |
#           ---------
#             \   /
#               *      __      __
#       ______________/  \    /  \_________
#                         \__/
#


m_width  = 0.85
m_height = 0.3
m_Z      = 0.9*0.5

k_length = 0.3
k_height  = 0.02
c_width  = 0.02

d  =  0.05
d0 = -0.1


with plt.xkcd():

    # Create a new figure
    fig, ax = plt.subplots()

    # Bottom triangle
    floorl = plt.Line2D((- m_width / 2 , 0), (0, d0), color='black', linewidth=2)
    floorr = plt.Line2D((  m_width / 2 , 0), (0, d0), color='black', linewidth=2)
    floor  = plt.Line2D((- m_width / 2 ,  m_width / 2 ), ( 0, 0), color='black', linewidth=2)
    ax.add_line(floorl)
    ax.add_line(floorr)
    ax.add_line(floor)

    # Mass 
    mu = patches.Rectangle((- m_width / 2, m_Z), m_width, m_height, linewidth=1, edgecolor='black', facecolor='red')
    ax.add_patch(mu)
    ax.text( 0, m_Z+0.5*m_height, '$m$', fontsize=16, ha='center')  # Text at position (2, 4) with 'Point A' label

    

    # Spring
    mul=1.3
    repetitions = 10 # Number of repetitions

    k1w_x = np.tile(np.array([- m_width / 4 - d,  -m_width / 4 +d ]), repetitions)
    k1w_y = np.linspace(0, m_Z, len(k1w_x))
    ax.text( (- m_width / 4 - d)*mul , 0.5*m_Z, '$k_{w1}$', fontsize=16, ha='right')  # Text at position (2, 4) with 'Point A' label


    ax.plot(k1w_x, k1w_y, color='black', linewidth=2)


    # Damper

    y_middle2 = 0.5*(d+m_Z)
    dampler_u_top2  = plt.Line2D((m_width / 4 ,     m_width / 4),     (0, y_middle2), color='black', linewidth=2)
    dampler_u_down2 = plt.Line2D((m_width / 4 ,     m_width / 4),     (m_Z, y_middle2), color='black', linewidth=2)
    dampler_u_q2    = plt.Line2D((m_width / 4 - d , m_width / 4 + d), (y_middle2, y_middle2), color='black', linewidth=2)
    dampler_u_ql2   = plt.Line2D((m_width / 4 - d , m_width / 4 - d), (y_middle2, y_middle2*1.15), color='black', linewidth=2)
    dampler_u_qr2   = plt.Line2D((m_width / 4 + d , m_width / 4 + d), (y_middle2, y_middle2*1.15), color='black', linewidth=2)
    ax.add_line(dampler_u_top2)
    ax.add_line(dampler_u_down2)
    ax.add_line(dampler_u_q2)
    ax.add_line(dampler_u_ql2)
    ax.add_line(dampler_u_qr2)


    ax.text( ( m_width / 4 + d)*mul , 0.5*m_Z, '$c$', fontsize=16, ha='left')  # Text at position (2, 4) with 'Point A' label

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
    plt.savefig('../images/quarter_car_one_dof.png')
    plt.show()

