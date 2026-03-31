"""
Motorbike Chassis Visualization
===============================

"""

import pyvista as pv

from pymycar.Cad.geometric_forms import rectangle_U, control_arm, simple_tube, simple_sphere, spring, rocked

def frame_cad_base(data, index=None):
    """
    Generate a control arm.

    Parameters
    ----------
    uca_front : array-like
        Coordinates of the front point of the control arm.
    uca_rear : array-like
        Coordinates of the rear point of the control arm.
    uca_outer_i : array-like
        Coordinates of the outer point of the control arm.
    radius : float, optional
        Radius of the Tubes, by default 10.
    resolution : int, optional
        Resolution of the Tubes, by default 100.
    n_sides : int, optional
        Number of sides of the Tubes, by default 10.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing two Tubes representing the control arm.

    Notes
    -----
    The control arm is formed by two Tubes connecting the front and rear points
    to the outer point.

    """

    e1 = simple_tube(data["SA_RIGHT"], data["SA_LEFT"])
    e2 = simple_tube(data["STEERING_AXIS_TOP"], data["STEERING_AXIS_BOTTOM"])
    e3 = control_arm(data["SA_RIGHT"], data["SA_LEFT"], data["STEERING_AXIS_BOTTOM"])
    e4 = control_arm(data["SA_RIGHT"], data["SA_LEFT"], data["STEERING_AXIS_TOP"])

    cad = pv.MultiBlock([e1, e2, e3, e4])
    return cad
