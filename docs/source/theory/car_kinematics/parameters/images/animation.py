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


import os
import time

###############################################################################
# Import from pymycar package
# ---------------------------
from pymycar.Cad.Car.frame import formula, model_B, model_C
# from pymycar.Cad.Wheel import wheel_cad
import pymycar


# def wheel_cad(data, wheel_variables, index=None):
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

# Create a directory to save frames
output_dir = "animation_frames"
os.makedirs(output_dir, exist_ok=True)

chassis = formula(front_axle_to_com=1500,
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

# Initial coordinates for the wheels
coordinate_right_wheel = np.array([1500, 1500/2, 156.5])
coordinate_left_wheel = np.array([1500, -1500/2, 156.5])

# Chassis model
chassis_tourist_A = model_B()

# Define the specific point location for the reference coordinate system
reference_point = np.array([0, 0, 400])

# Create a ground plane
ground = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=5000, j_size=5000)

# Create the plotter
plotter = pv.Plotter(off_screen=True)

# Add static meshes
plotter.add_mesh(chassis_tourist_A, color="red", opacity=0.5)
plotter.add_mesh(ground, color="blue", opacity=0.5)

# Animation loop
for i, camber in enumerate(np.linspace(0.0, 1.0, num=100)):
    direction_right_wheel = np.array([0, 1, camber])
    direction_left_wheel = np.array([0, 1, -camber])

    wheel_right = pv.Cylinder(center=coordinate_right_wheel, direction=direction_right_wheel, height=200, radius=400)
    plane_right = pv.Plane(center=coordinate_right_wheel, direction=direction_right_wheel, i_size=1200, j_size=1200)

    wheel_left = pv.Cylinder(center=coordinate_left_wheel, direction=direction_left_wheel, height=200, radius=400)
    plane_left = pv.Plane(center=coordinate_left_wheel, direction=direction_left_wheel, i_size=1200, j_size=1200)

    # Clear previous meshes
    plotter.clear()

    # Add updated meshes
    plotter.add_mesh(chassis_tourist_A, color="red", opacity=0.5)
    plotter.add_mesh(ground, color="blue", opacity=0.5)
    plotter.add_mesh(wheel_right, color="black", opacity=1.0)
    plotter.add_mesh(wheel_left, color="black", opacity=1.0)
    plotter.add_mesh(plane_right, color="blue", opacity=0.5)
    plotter.add_mesh(plane_left, color="blue", opacity=0.5)

    # Render the scene
    plotter.render()

    # Save the frame
    frame_filename = os.path.join(output_dir, f"frame_{i:03d}.png")
    plotter.screenshot(frame_filename)

    # Pause to create animation effect
    time.sleep(0.1)

# Show the final plot
plotter.show()