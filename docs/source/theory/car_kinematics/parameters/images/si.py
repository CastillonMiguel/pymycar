"""
.. _ref_plot_chassis_new:

Chassis: new
^^^^^^^^^^^^

This example demonstrates the use of excitation functions.

"""

###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np
import pandas as pd
import pymycar
import pyvista as pv


###############################################################################
# Import from pymycar package
# ---------------------------
from pymycar.Cad.Chassis.formula import model_A, model_B
# from pymycar.Cad.Wheel import car_wheel
import pymycar


# def car_wheel(data, wheel_variables, index=None):
#     """
#     Creates a 3D wheel model based on input data and orientation variables.

#     Parameters
#     ----------
#     data : dict
#         Dictionary containing suspension geometry data.
#     wheel_variables : dict
#         Dictionary containing wheel orientation variables such as kingpin, caster,
#         and camber angles.
#     index : int
#         Index of the current data point.

#     Returns
#     -------
#     pyvista.MultiBlock
#         A PyVista MultiBlock containing the wheel mesh.
#     """
#     wheel = pv.Cylinder(center=data["wheel_center"][index], direction=(0, 1, 0), height=80, radius=100)
  
#     angle_x = np.rad2deg(wheel_variables["toe_angle"][index])
#     angle_y = np.rad2deg(wheel_variables["side_view_angle"][index])
#     angle_z = np.rad2deg(wheel_variables["camber_angle"][index])


#     wheel.rotate_z(angle_z, inplace=True)
#     wheel.rotate_y(angle_y, inplace=True)
#     wheel.rotate_x(angle_x, inplace=True)

    
#     return pv.MultiBlock([wheel])


chassis = model_A(front_axle_to_com=1500,
            rear_axle_to_com=1645*0.5,
            front_track=1500*0.5,
            rear_track=1645*0.5,
            com_height=400.0,
            roll=0,
            pitch=0,
            yaw=0,
            x=0,
            y=0,
            z=0)


# Create a ground plane
ground = pv.Plane(center=(0, 0, -220), direction=(0, 0, 1), i_size=5000, j_size=5000)
plane_center = pv.Plane(center=np.array([0, 0, 0]), direction=(0, 1, 0), i_size=2000, j_size=5000)

coorinate_right_wheel = np.array([1500, 1500/2, 156.5])
coorinate_left_wheel = np.array([1500, -1500/2, 156.5])

coorinate_rear_right_wheel = np.array([-1000, 1.3*1500/2, 156.5])
coorinate_rear_left_wheel = np.array([-1200, -1.2*1500/2, 156.5])


type_angle = "side"

camber = 0.0
toe = 0.0
side = -0.5
if type_angle == "camber":
    direction_right_wheel = np.array([0, 1, camber])
    direction_left_wheel = np.array([0, 1, -camber])
if type_angle == "toe":
    direction_right_wheel = np.array([1, toe, 0])
    direction_left_wheel = np.array([1, -toe, 0])
if type_angle == "side":
    direction_right_wheel = np.array([0, 1, 0])
    direction_left_wheel = np.array([0, 1,  0])
    
direction_rear_right_wheel = np.array([0, 1, 0])
direction_rear_left_wheel = np.array([0, 1, 0])

wheel_right = pv.Cylinder(center=coorinate_right_wheel, direction=direction_right_wheel, height=200, radius=400)

plane_right = pv.Plane(center=coorinate_right_wheel, direction=direction_right_wheel, i_size=1200, j_size=1200)

wheel_left  = pv.Cylinder(center=coorinate_left_wheel, direction=direction_left_wheel, height=200, radius=400)
plane_left  = pv.Plane(center=coorinate_left_wheel, direction=direction_left_wheel, i_size=1200, j_size=1200)

if type_angle == "side":
    plane_right = pv.Plane(center=coorinate_right_wheel, direction=np.array([1, 0, side]), i_size=1200, j_size=1200)
    plane_left  = pv.Plane(center=coorinate_left_wheel, direction=np.array([1, 0, side]), i_size=1200, j_size=1200)

wheel_rear_right = pv.Cylinder(center=coorinate_rear_right_wheel, direction=direction_rear_right_wheel, height=300, radius=400)
wheel_rear_left = pv.Cylinder(center=coorinate_rear_left_wheel, direction=direction_rear_left_wheel, height=300, radius=400)
# wheel_right = car_wheel(data, wheel_variables, index=None)

chassis_tourist_A = pymycar.Cad.Chassis.tourist.model_A()

# Define the specific point location for the reference coordinate system
reference_point = np.array([0, 0, 400])


plotter = pv.Plotter()
plotter.add_mesh(ground, color="black", opacity=0.5)
plotter.add_mesh(chassis, color="red", opacity=0.5)
plotter.add_mesh(wheel_right, color="black", opacity=1.0)
plotter.add_mesh(wheel_left, color="black", opacity=1.0)
plotter.add_mesh(wheel_rear_right, color="black", opacity=1.0)
plotter.add_mesh(wheel_rear_left, color="black", opacity=1.0)

# plotter.add_mesh(plane_right, color="green", opacity=0.5)
# plotter.add_mesh(plane_left, color="green", opacity=0.5)

plotter.add_mesh(plane_right, color="blue", opacity=0.5)
plotter.add_mesh(plane_left, color="blue", opacity=0.5)

# plotter.add_mesh(plane_right, color="black", opacity=0.5)
# plotter.add_mesh(plane_left, color="black", opacity=0.5)

# plotter.add_mesh(plane_center, color="red", opacity=0.5)
plotter.show()
