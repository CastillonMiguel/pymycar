r"""

.. _ref_cad_motorbike_front_assembly_forks:

Front Assembly: Front Suspension Forks Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    #
    #
    #    fork_left_upper *       
    #                    |    * STEERING_AXIS_TOP    
    #                    |     \                        
    #                    |      * STEERING_AXIS_BOTTOM                       
    #                    |                 
    #                    |         * fork_right_upper    
    #                    |         |                
    #   fork_left_middle *         | 
    #                    |         |
    #                    |         |
    #                    |         |
    #  fork_left_bottom  *         * fork_right_middle 
    #                      \       |  
    #                       \      |
    #           wheel_center *     |
    #                          \   |   
    #                            \ |
    #                              *fork_right_bottom
    #                     
    #         
    #

+-------------------------+----------------------------------+--------+
| Points Name             | Description                      | Type   |
+=========================+==================================+========+
| wheel_center_front      | Center of the Wheel              | mobile |
+-------------------------+----------------------------------+--------+
| STEERING_AXIS_TOP       | Steering axis top point          | fixed  |
+-------------------------+----------------------------------+--------+
| STEERING_AXIS_BOTTOM    | Steering axis bottom point       | fixed  |
+-------------------------+----------------------------------+--------+
| fork_right_upper        | Fork right upper attachment      | mobile |
+-------------------------+----------------------------------+--------+
| fork_left_upper         | Fork left upper attachment       | mobile |
+-------------------------+----------------------------------+--------+
| fork_right_middle       | Fork right middle attachment     | mobile |
+-------------------------+----------------------------------+--------+
| fork_left_middle        | Fork left middle attachment      | mobile |
+-------------------------+----------------------------------+--------+
| fork_right_bottom       | Fork right bottom attachment     | mobile |
+-------------------------+----------------------------------+--------+
| fork_left_bottom        | Fork left bottom attachment      | mobile |
+-------------------------+----------------------------------+--------+

"""

###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np
import pyvista as pv

from pymycar.Cad.MotorCycle.front_assembly import fork_front_suspension

###############################################################################
# Parameters Definition
# ---------------------
data = {
    "wheel_center_front": np.array([1100.0,   0.0,     0.0]),
    "STEERING_AXIS_TOP": np.array([900.0, 0.0, 600.0]),
    "STEERING_AXIS_BOTTOM": np.array([1000.0, 0.0, 500.0]),
    "fork_right_upper": np.array([900.0, -200.0, 600.0]),
    "fork_left_upper": np.array([900.0, 200.0, 600.0]),
    # "fork_right_middle": np.array([999.0, -200.0, 300.0]),
    # "fork_left_middle": np.array([999.0, 200.0, 300.0]),
    "fork_right_bottom": np.array([1100.0, -200.0, 0.0]),
    "fork_left_bottom": np.array([1100.0, 200.0, 0.0]),
}

wheel = pv.Cylinder(center=data["wheel_center_front"], direction=(0, 1, 0), height=50, radius=200)
wheel = pv.ParametricTorus(ringradius=200, crosssectionradius=80).translate(data["wheel_center_front"]).rotate_x(90)

bar_right_top,  U_form_upper, U_form_bottom = fork_front_suspension(data)


plotter = pv.Plotter()
plotter.add_mesh(wheel, color="black", opacity=1.0)
plotter.add_mesh(bar_right_top, color="red")
plotter.add_mesh(U_form_upper, color="blue")
plotter.add_mesh(U_form_bottom, color="green")


# Add points to the plot
for name, coord in data.items():
    plotter.add_mesh(pv.Sphere(radius=5, center=coord), color='red')

# Add text annotations
for name, coord in data.items():
    plotter.add_point_labels([coord], [name], point_size=20, font_size=30, text_color='black', always_visible=True)

plotter.show()
