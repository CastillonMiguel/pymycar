"""
Wheel
=====

"""

import pyvista as pv
import numpy as np

def motorcycle_wheel(center, point_a, point_b, ringradius, crosssectionradius):
    """
    Create a PyVista Torus whose orientation is defined by the direction 
    between two points, passing through the center.

    Parameters
    ----------
    center : array-like
        Torus center [x, y, z].
    point_a : array-like
        First point defining the direction.
    point_b : array-like
        Second point defining the direction.
    ringradius : float
        Torus ring radius.
    crosssectionradius : float
        Torus cross-section radius.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing the Torus mesh.
    """

    direction = np.array(point_b) - np.array(point_a)
    norm = np.linalg.norm(direction)
    if norm == 0:
        raise ValueError("point_a and point_b cannot be the same point (direction length is zero).")
    direction = direction / norm

    # By default, a ParametricTorus has its normal along the Z-axis [0, 0, 1]
    torus = pv.ParametricTorus(ringradius=ringradius, crosssectionradius=crosssectionradius)

    z_axis = np.array([0.0, 0.0, 1.0])
    
    # Align the Torus Z-axis with the calculated direction vector
    if np.allclose(direction, z_axis):
        pass
    elif np.allclose(direction, -z_axis):
        torus.rotate_vector([1.0, 0.0, 0.0], 180.0, inplace=True)
    else:
        rot_axis = np.cross(z_axis, direction)
        rot_angle = np.degrees(np.arccos(np.clip(np.dot(z_axis, direction), -1.0, 1.0)))
        torus.rotate_vector(rot_axis, rot_angle, inplace=True)

    torus.translate(center, inplace=True)

    return pv.MultiBlock([torus])
