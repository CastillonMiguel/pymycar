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
zz = -400

ground = pv.Plane(center=(0, 0, -300 + zz), direction=(0, 0, 1), i_size=5000, j_size=5000)
plane_center = pv.Plane(center=np.array([0, 0, 0]), direction=(0, 1, 0), i_size=2000, j_size=5000)
plane_center2 = pv.Plane(center=np.array([0, 0, 0]), direction=(0, 0, 1), i_size=2000, j_size=5000)

coorinate_right_wheel = np.array([1500, 1500/2, 156.5 + zz])
coorinate_left_wheel = np.array([1500, -1500/2, 156.5 + zz])
coorinate_rear_right_wheel = np.array([-1000, 1.3*1500/2, 156.5+zz])
coorinate_rear_left_wheel = np.array([-1200, -1.2*1500/2, 156.5+zz])


xube = 500
xube_z = 250

wheel_right = pv.Cube(center=coorinate_right_wheel,  x_length=xube, y_length=xube, z_length=xube_z)
wheel_left  = pv.Cube(center=coorinate_left_wheel,  x_length=xube, y_length=xube, z_length=xube_z)
wheel_rear_right = pv.Cube(center=coorinate_rear_right_wheel,  x_length=xube, y_length=xube, z_length=xube_z)
wheel_rear_left = pv.Cube(center=coorinate_rear_left_wheel, x_length=xube, y_length=xube, z_length=xube_z)

cog = pv.Sphere(center=(0, 0, 400), radius=50)

chassis_tourist_A = pymycar.Cad.Chassis.tourist.model_A()

# Define the specific point location for the reference coordinate system
reference_point = np.array([0, 0, 400])


plotter = pv.Plotter()
# plotter.add_mesh(ground, color="black", opacity=0.5)
plotter.add_mesh(cog, color="black", opacity=0.5)

plotter.add_mesh(chassis, color="red", opacity=0.5)
plotter.add_mesh(wheel_right, color="black", opacity=0.5, name="Tie Rod Tube")
plotter.add_mesh(wheel_left, color="black", opacity=0.5)
plotter.add_mesh(wheel_rear_right, color="black", opacity=0.5)
plotter.add_mesh(wheel_rear_left, color="black", opacity=0.5)

# plotter.add_mesh(plane_center, color="red", opacity=0.5)

plotter.add_point_labels([coorinate_right_wheel], ["m_u1"], point_size=20, font_size=30, text_color='black', always_visible=True)
plotter.add_point_labels([coorinate_left_wheel], ["m_u2"], point_size=20, font_size=30, text_color='black', always_visible=True)
plotter.add_point_labels([coorinate_rear_right_wheel], ["m_u3"], point_size=20, font_size=30, text_color='black', always_visible=True)
plotter.add_point_labels([coorinate_rear_left_wheel], ["m_u4"], point_size=20, font_size=30, text_color='black', always_visible=True)

plotter.show()

