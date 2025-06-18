"""
.. _ref_plot_spring:

Spring
^^^^^^

"""

import numpy as np
import pyvista as pv

# Define the points for the tube
tierod_inner = np.array([830.0, -280.00, 250.0])
tierod_outer_i = np.array([850.0, -420.00, 75.0])
resolution = 100
radius = 10.0
n_sides = 10

# Create the tube
e5 = pv.Tube(tierod_inner, tierod_outer_i, resolution, radius, n_sides)

# Calculate the direction and length of the tube
direction = tierod_outer_i - tierod_inner
length = np.linalg.norm(direction)
direction = direction.astype(float) / length

# Calculate a perpendicular direction
if np.allclose(direction, [0, 0, 1]):
    perpendicular = np.array([1, 0, 0])
else:
    reference_vector = np.array([0, 0, 1])
    perpendicular = np.cross(direction, reference_vector)
    perpendicular /= np.linalg.norm(perpendicular)

# Create a polygon to represent the cross-section of the coil
coil_radius = 0.1  # Adjust the coil radius as needed
profile = pv.Polygon(
    center=tierod_inner,
    radius=coil_radius / 5,  # Smaller radius for the coil
    normal=perpendicular,
    n_sides=30,
)

# Create the helical shape using extrude_rotate
n_coils = 10
n_points = 100
angle = 360 * n_coils
coil = profile.extrude_rotate(
    resolution=n_points,
    translation=length,
    dradius=0.0,
    angle=angle,
    capping=False,
    rotation_axis=direction
)

# Translate the coil to align with the tube
coil.translate(tierod_inner)

# Plot the tube and the coil
plotter = pv.Plotter()
plotter.add_mesh(e5, color="blue")
plotter.add_mesh(coil, color="red")
plotter.show()