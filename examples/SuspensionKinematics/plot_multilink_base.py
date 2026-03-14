r"""
.. _ref_100:

Double Whisbonebase
^^^^^^^^^^^^^^^^^^^

.. code-block::

   #                        
   #                    \\\    
   #                    \-/  
   #             UCA_REAR* 
   #                    /
   #                   / 
   #   -----------    /
   #    |       |    /
   #    |       |   *----------*UCA_FRONT
   #    |       |             /⁻\.
   #    |       |             ///
   #    |       |
   #    |       |
   #    |       |        tierod_outer
   #    |       |       *--------------------*TIEROD_INNER
   #    |       |
   #    |       |
   #    |       |       lca_outer
   #    |       |      *------------*LCA_REAR
   #   -----------     \           /⁻\.
   #                    \          ///
   #                     \.
   #                      *LCA_FRONT
   #                     /⁻\.
   #                     ///
   

+--------------+-------------------------------+
| Name         | Description                   | 
+==============+===============================+
| UCA_FRONT    | upper control arm front       | 
+--------------+-------------------------------+
| UCA_REAR     | upper control arm rear        | 
+--------------+-------------------------------+
| LCA_FRONT    | upper control arm front       | 
+--------------+-------------------------------+
| LCA_REAR     | LOWER control arm rear        | 
+--------------+-------------------------------+
| TIEROD_INNER | tierod inner                  | 
+--------------+-------------------------------+
| uca_outer    | upper control arm outer       |
+--------------+-------------------------------+
| lca_outer    | lower upper control arm outer |  
+--------------+-------------------------------+
| tierod_outer | tierod outer                  |
+--------------+-------------------------------+


"""

###############################################################################
# Import necessary libraries
# --------------------------
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyvista as pv


###############################################################################
# Import from pymycar package
# ---------------------------
from pymycar.SuspensionKinematic.multilink import multilink
from pymycar.SuspensionKinematic.functions import get_wheel
from pymycar.Cad.Wheel.wheel import wheel_cad

from pymycar.Cad.Wheel.wheel import wheel_cad
from pymycar.Cad.Suspension.multilink import multilink_cad_base

###############################################################################
# Parameters Definition
# ---------------------
data = {
    "UCA_FRONT": np.array([4707.1, -462.7, 1120.5]),
    "UCA_REAR": np.array([4912.2, -418.5, 1128.2]), 
    "LCA_FRONT": np.array([4066.2, -498.8, 1015.7]),
    "LCA_REAR": np.array([4682.3, -285.2, 936.4]), 
    "TIEROD_INNER": np.array([5042.5, -272.4, 988.7]),
    "uca_outer": np.array([4701.2, -710.5, 1207.3]),   
    "lca_outer": np.array([4687.4, -698.2, 927.5]),   
    "tierod_outer": np.array([4942.9, -719.8, 1038.2]),
    "wheel_center": np.array([4682.2, -766.1, 1047.4]),
    "uca_outer_aux": np.array([4840.7, -721.2, 1202.8]),   
    "lca_outer_aux": np.array([4702.5, -701.7, 1006.2]),  
}


###############################################################################
# Call the Solver
# ---------------
solution, wheel_variables = multilink(data,
                     max_height_increase=100,
                     max_height_decrease=100,
                     height_step=1,
                     save_to_txt=True,
                     result_folder_name="multilink",
                     path=None)





###############################################################################
# Plot: "wheel_track vs "wheel_jounce"
# ------------------------------------
fig, ax = plt.subplots() 
ax.plot(wheel_variables["wheel_jounce"], wheel_variables["wheel_track"], 'k-', linewidth=2.0)
ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('wheel track') 
ax.set_ylabel('caster angle')    
ax.set_title('Wheel Jounce - Wheel Track')


###############################################################################
# Plot: "wheel_base" vs "wheel_jounce"
# ------------------------------------
fig, ax = plt.subplots() 
ax.plot(wheel_variables["wheel_jounce"], wheel_variables["wheel_base"], 'k-', linewidth=2.0)
ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('wheel jounce')  
ax.set_ylabel('wheel base')  
ax.set_title('Wheel Jounce - Wheel Base')


###############################################################################
# Plot: "camber_angle" vs "wheel_jounce"
# --------------------------------------
fig, ax = plt.subplots() 
ax.plot(wheel_variables["wheel_jounce"], wheel_variables["camber_angle"],'r-', linewidth=2.0)
ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('wheel jounce')
ax.set_ylabel('camber angle')
ax.set_title('Wheel Jounce - Camber Angle')


###############################################################################
# Plot: "camber_angle" vs "wheel_jounce"
# --------------------------------------
fig, ax = plt.subplots() 
ax.plot(wheel_variables["wheel_jounce"], wheel_variables["side_view_angle"],'r-', linewidth=2.0)
ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('wheel jounce')
ax.set_ylabel('side view angle')
ax.set_title('Wheel Jounce - Side View Angle')


###############################################################################
# Plot: "camber_angle" vs "wheel_jounce"
# --------------------------------------
fig, ax = plt.subplots() 
ax.plot(wheel_variables["wheel_jounce"], wheel_variables["toe_angle"],'r-', linewidth=2.0)
ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('wheel jounce')
ax.set_ylabel('toe angle')
ax.set_title('Wheel Jounce - Toe Angle')


###############################################################################
# Plot: "caster_angle" vs "wheel_jounce"
# --------------------------------------
fig, ax = plt.subplots() 
ax.plot(wheel_variables["wheel_jounce"], wheel_variables["caster_angle"], 'g-', linewidth=2.0)
ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('wheel jounce')  
ax.set_ylabel('caster angle')    
ax.set_title('Wheel Jounce - Caster Angle') 


###############################################################################
# Plot: kingpin_angle vs "wheel_jounce"
# ------------------------------------
fig, ax = plt.subplots() 
ax.plot( wheel_variables["wheel_jounce"], wheel_variables["kingpin_angle"], 'g-', linewidth=2.0)
ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('wheel jounce') 
ax.set_ylabel('kingpin angle')
ax.set_title('Wheel Jounce - Kingpin Angle')


plt.show()


# last_meshes = []
# def plot_frame(plotter, data, index=None):
#     global last_meshes

#     if index is None:
#         index = data["index_reference"]

#     upper_control_arm, lower_control_arm, upper_control_arm_aux, lower_control_arm_aux, direction, wheel_center1 = multilink_cad_base(data,index)
#     wheel = wheel_cad(data, wheel_variables, index)
    
#     # Remove the last meshes
#     for mesh in last_meshes:
#         plotter.remove_actor(mesh)

#     # Add new meshes
#     last_meshes = [
#         plotter.add_mesh(wheel_center1, color="black"),
#         plotter.add_mesh(upper_control_arm, color="blue"),
#         plotter.add_mesh(lower_control_arm, color="pink"),
#         plotter.add_mesh(direction, color="green"),
#         plotter.add_mesh(wheel, color="black", opacity=0.5),
#         plotter.add_mesh(upper_control_arm_aux, color="blue"),
#         plotter.add_mesh(lower_control_arm_aux, color="pink"),
#     ]


# plotter = pv.Plotter()
# def create_mesh(value):
#     res = np.abs(solution["wheel_center"][:,2] - value).argmin()
#     plot_frame(plotter, solution, index=res)

# plotter.add_slider_widget(create_mesh,
#                           rng=[solution["wheel_center"][0, 2], solution["wheel_center"][-1, 2]],
#                           value=solution["wheel_center"][solution["index_reference"]][2],
#                           title='Jounce')
# plotter.show()

