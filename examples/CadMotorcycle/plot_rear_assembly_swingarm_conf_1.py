r"""
.. _ref_cad_motorbike_rear_assembly_swingarm_conf_1:

Rear Assembly: Swingarm Configuration 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

   #                          
   #                                  *U_SPRING_MOUNT
   #                                 /                   \ 
   #                                .                     . 
   #                               /                       \ 
   #        /--------------       .         ___________-----* SA_LEFT
   #       /                     /         /              /⁻\\ 
   #      /                 ___ .________/                /// \ 
   #     / sa_left_outer  /    /                               \ 
   #    /     *----------/    *               ___________-------* SA_RIGHT
   #    \      \            l_spring_mount   /                 /⁻\\ 
   #  wheel center*            _____________/                  /// . 
   #     \       \            /                                     \  
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
| U SPRING MOUNT  | Upper spring mount       | fixed  |
+-----------------+--------------------------+--------+
| l spring mount  | lower spring mount       | mobile |
+-----------------+--------------------------+--------+

"""

###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np
from pymycar.Cad.geometric_forms import simple_spring
import pyvista as pv

from pymycar.Cad.MotorCycle.rear_assembly import swinarm_cad_base
from pymycar.Cad.MotorCycle.frame import frame_cad_base
from pymycar.Cad.MotorCycle.rear_assembly import rear_suspension_cantilever
from pymycar.Cad.MotorCycle.front_assembly import fork_front_suspension

data = {
    "SA_RIGHT": np.array([0.0, -100.0, 0.0]),
    "SA_LEFT": np.array([0.0,   200.0,  0.0]),    
    "sa_right_outer": np.array([-500.0, -125.0, -0.0]),
    "sa_left_outer": np.array([-500.0,   125.0, -0.0]),
    "wheel_center": np.array([-500.0,   0.0,    -0.0]),
    "U_SPRING_MOUNT": np.array([-100.0, 0.0, 300.0]),
    "l_spring_mount": np.array([-250.0, 0.0, 0.0]),
}


swingarm = swinarm_cad_base(data, index=None)
wheel = pv.Cylinder(center=data["wheel_center"], direction=(0, 1, 0), height=50, radius=200)
suspension = rear_suspension_cantilever(data, index=None)

# from pymycar.Cad.geometric_forms import spring, simple_spring
# suspension = simple_spring(data["U_SPRING_MOUNT"], data["l_spring_mount"][None])
plotter = pv.Plotter()
plotter.add_mesh(swingarm, color="blue"),
plotter.add_mesh(wheel, color="black", opacity=0.5)
plotter.add_mesh(suspension, color="green")


# Add points to the plot
for name, coord in data.items():
    plotter.add_mesh(pv.Sphere(radius=5, center=coord), color='red')

# Add text annotations
for name, coord in data.items():
    plotter.add_point_labels([coord], [name], point_size=20, font_size=30, text_color='black', always_visible=True)


plotter.show()
