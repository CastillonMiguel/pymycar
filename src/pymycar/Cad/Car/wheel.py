"""
Wheel
=====
"""

import pyvista as pv
import numpy as np

def car_wheel(data, index=None):
    """
    Create a PyVista cylindrical representation of a car wheel, oriented
    according to a direction defined by two reference points.

    The cylinder axis is aligned with the vector defined by
    (wheel_center_axis - uca_outer) and then translated to the wheel center.

    Parameters
    ----------
    data : dict
        Dictionary containing simulation geometry data. It must include:
        - "wheel_center"
        - "wheel_center_axis"

    index : int, optional
        Index of the configuration step to extract the points.

    Returns
    -------
    pv.MultiBlock
        A MultiBlock containing the oriented cylinder mesh representing the wheel.

    Notes
    -----
    - The cylinder is initially generated aligned with the Z-axis.
    - It is then rotated to match the direction defined by
      (point_b - point_a).
    - Finally, it is translated to the wheel center position.
    - This function is intended for kinematic visualization of wheel motion
      in suspension systems.
    """
    radius, height = 100, 20

    point_a = data["wheel_center"][index]
    point_b = data["wheel_center_axis"][index]
    center = data["wheel_center"][index]

    direction = np.array(point_b) - np.array(point_a)
    norm = np.linalg.norm(direction)
    if norm == 0:
        raise ValueError("point_a and point_b cannot be the same point.")

    direction = direction / norm

    # Create default cylinder aligned with Z-axis
    cyl = pv.Cylinder(
        center=(0, 0, 0),
        direction=(0, 0, 1),
        radius=radius,
        height=height
    )

    z_axis = np.array([0.0, 0.0, 1.0])

    if np.allclose(direction, z_axis):
        pass
    elif np.allclose(direction, -z_axis):
        cyl.rotate_vector([1, 0, 0], 180, inplace=True)
    else:
        rot_axis = np.cross(z_axis, direction)
        rot_angle = np.degrees(np.arccos(np.clip(np.dot(z_axis, direction), -1.0, 1.0)))
        cyl.rotate_vector(rot_axis, rot_angle, inplace=True)

    cyl.translate(center, inplace=True)

    return pv.MultiBlock([cyl])


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