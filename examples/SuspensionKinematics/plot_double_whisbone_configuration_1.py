r"""
.. _ref_1712:

Double Whisbone
^^^^^^^^^^^^^^^


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
    #    |       |             /⁻\
    #    |       |             ///
    #    |       |
    #    |       |
    #    |       |        tierod_outer
    #    |       |       *--------------------*TIEROD_INNER
    #    |       |
    #    |       |
    #    |       |       lca_outer
    #    |       |      *------------*LCA_REAR
    #   -----------     \           /⁻\
    #                    \          ///
    #                     \
    #                      *LCA_FRONT
    #                     /⁻\
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
| TIEROD_INNER |  tierod inner                 | 
+--------------+-------------------------------+
| uca_outer    | upper control arm outer       |
+--------------+-------------------------------+
| lca_outer    | lower upper control arm outer |  
+--------------+-------------------------------+
| tierod_outer | tierod outer                  |
+--------------+-------------------------------+


"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyvista as pv

from pymycar.SuspensionKinematic.double_whisbone  import double_whisbone_configuration_1

from pymycar.Cad.Suspension.double_whisbone import whisbone_cad_configuration_1
from pymycar.Cad.Wheel.wheel import wheel_cad

# Points
data = {
    "UCA_FRONT": np.array([586.7, -314.5, 199.9]),
    "UCA_REAR": np.array([930.7, -230.2, 244.2]), 
    "LCA_FRONT": np.array([588.7, -384.2, 76.8]),
    "LCA_REAR": np.array([938.2, -191.2, 62.7]), 
    "TIEROD_INNER": np.array([934.2, -192.1, 81.2]),
    "uca_outer": np.array([953.0, -474.2, 272.2]),   
    "lca_outer": np.array([934.8, -514.7, 47.9]),   
    "tierod_outer": np.array([1027.1, -513.7, 43.6]),
    "wheel_center": np.array([941.5, -580.2, 155.1]),
    "U_SPRING_MOUNT": np.array([831.7, -278.7, 251.2]),
    "l_spring_mount": np.array([849.2, -419.1, 76.4])
}


###############################################################################
# Call the Solver
# ---------------



solution, wheel_variables = double_whisbone_configuration_1(data,
                                           max_height_increase=50,
                                           max_height_decrease=20,
                                           height_step=1,
                                           save_to_txt=True,
                                           result_folder_name="double_whisbone_configuration_1",
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

#     upper_control_arm, lower_control_arm, direction, wheel_center1, spring_o = whisbone_cad_configuration_1(data,index)
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
#         plotter.add_mesh(spring_o, color="red")
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