"""
Wheel
=====
"""

import pyvista as pv
import numpy as np

def wheel_cad(data, wheel_variables, index=None):
    """
    Creates a 3D wheel model based on input data and orientation variables.

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data.
    wheel_variables : dict
        Dictionary containing wheel orientation variables such as kingpin, caster,
        and camber angles.
    index : int
        Index of the current data point.

    Returns
    -------
    pyvista.MultiBlock
        A PyVista MultiBlock containing the wheel mesh.
    """
    wheel = pv.Cylinder(data["wheel_center"][index], direction=(0, 1, 0), height=80, radius=100)
  
    angle_x = np.rad2deg(wheel_variables["toe_angle"][index])
    angle_y = np.rad2deg(wheel_variables["side_view_angle"][index])
    angle_z = np.rad2deg(wheel_variables["camber_angle"][index])


    wheel.rotate_z(angle_z, inplace=True)
    wheel.rotate_y(angle_y, inplace=True)
    wheel.rotate_x(angle_x, inplace=True)

    
    return pv.MultiBlock([wheel])