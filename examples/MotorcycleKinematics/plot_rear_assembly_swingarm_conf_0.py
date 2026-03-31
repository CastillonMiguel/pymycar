r"""
.. _ref_MotorcycleKinematics_rear_assembly_swingarm_conf_0:

Rear Assembly: Swingarm Configuration 0
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

   #                          
   #
   #                                                  \ 
   #                                                   . 
   #                                                    \ 
   #        /--------------                ___________----* SA_LEFT
   #       /                              /             /⁻\\ 
   #      /                 _____________/              ///\ 
   #     / sa_left_outer  /                                 \ 
   #    /     *----------/                   ___________-----* SA_RIGHT
   #    \      \                             /              /⁻\\ 
   #  wheel center*            _____________/               /// . 
   #     \       \            /                                  \ 
   #      \       *----------/  
   #       \   SA_right_outer
   #        \
   #         \
   #          \---*----------
   #             Wheel center ground reference
   #

+-----------------+--------------------------+--------+
| Points  Name    | Description              | Type   |
+=================+==========================+========+
| wheel center    | Center of the Wheel      | mobile |
+-----------------+--------------------------+--------+
| SA RIGHT        | Swingarm Right           | fixed  |
+-----------------+--------------------------+--------+
| SA LEFT         | Swingarm Left            | fixed  |
+-----------------+--------------------------+--------+
| sa right outer  | Swingarm right outer     | mobile |
+-----------------+--------------------------+--------+
| sa left outer   | Swingarm left outer      | mobile |
+-----------------+--------------------------+--------+

"""

###############################################################################
# Import necessary libraries
# --------------------------
import os
import numpy as np

from pymycar.MotorCycleKinematic import rear_bike_base

###############################################################################
# Parameters Definition
# ---------------------
data = {
    # --- Front assembly ---
    "wheel_center_front": np.array([650.0,   0.0,   -520.0]),
    "STEERING_AXIS_BOTTOM": np.array([650.0, 0.0,  -100.0]),
    "STEERING_AXIS_TOP":    np.array([570.0, 0.0,  250.0]),
    "fork_right_upper":  np.array([570.0, -110.0, 250.0]),
    "fork_left_upper":   np.array([570.0,  110.0, 250.0]),
    "fork_right_bottom": np.array([650.0, -120.0, -520.0]),
    "fork_left_bottom":  np.array([650.0,  120.0, -520.0]),
    # --- Rear assembly ---
    "wheel_center_rear": np.array([-600.0,   0.0,  -520.0]),  
    "SA_RIGHT": np.array([-100.0, -90.0, -300.0]),           
    "SA_LEFT":  np.array([-100.0,  90.0, -300.0]),
    "sa_right_outer": np.array([-600.0, -110.0, -520.0]), 
    "sa_left_outer":  np.array([-600.0,  110.0, -520.0]),
    "U_SPRING_MOUNT": np.array([-150.0, 0.0,  50.0]),
    "l_spring_mount": np.array([-420.0, 0.0, -350.0]),
}
# file_path = 'data.suspgeo'
# data = load_defined_geometry("double_whisbone_base/input_geometry.suspgeo")

###############################################################################
# Call the Solver
# ---------------
solution, wheel_variables = rear_bike_base(data,
                                max_height_increase=100,
                                max_height_decrease=100, 
                                height_step=1.0,
                                save_to_txt=True,
                                result_folder_name="bike",
                                path = None)




import pyvista as pv
from pymycar.Cad.MotorCycle.rear_assembly import swinarm_cad_base
from pymycar.Cad.MotorCycle.frame import frame_cad_base


frame = frame_cad_base(data, index=None)

last_meshes = []
def plot_frame(plotter, data, index=None):
    global last_meshes

    if index is None:
        index = data["index_reference"]

    # swingarm, wheel_center1 = swingarm_cad_base(data, index)
    swingarm = swinarm_cad_base(data, index)
    # Remove the last meshes
    for mesh in last_meshes:
        plotter.remove_actor(mesh)

    # Add new meshes
    last_meshes = [

        # plotter.add_mesh(wheel_center1, color="black"),
        plotter.add_mesh(frame, color="red"),
        plotter.add_mesh(swingarm, color="blue"),
        # plotter.add_mesh(lower_control_arm, color="pink"),
        # plotter.add_mesh(direction, color="green"),
        # plotter.add_mesh(wheel, color="black", opacity=0.5)
    ]


plotter = pv.Plotter()
def create_mesh(value):
    res = np.abs(solution["wheel_center_rear"][:,2] - value).argmin()
    plot_frame(plotter, solution, index=res)

plotter.add_slider_widget(create_mesh,
                          rng=[solution["wheel_center_rear"][0, 2], solution["wheel_center_rear"][-1, 2]],
                          value=solution["wheel_center_rear"][solution["index_reference"]][2],
                          title='Jounce')
plotter.show()
