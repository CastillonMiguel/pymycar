"""
Motorbike Rear Assembly Visualization
=====================================

"""
import pyvista as pv
from pymycar.Cad.geometric_forms import rectangle_U, control_arm, simple_tube, simple_sphere, spring, rocked, simple_spring, rocked


def swingarm_cad_base(data, index=None):
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
    U_form = rectangle_U(data["SA_RIGHT"], data["SA_LEFT"], data["sa_right_outer"][index], data["sa_left_outer"][index], radius=10, resolution=100, n_sides=10)
    return U_form 


def rear_suspension_cantilever(data, index=None):
    """
    Creates a suspension system configuration with a spring.

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data.
    index : int
        Index of the current data point.

    Returns
    -------
    tuple
        A tuple containing:
        - upper_control_arm : pyvista.PolyData
        - lower_control_arm : pyvista.PolyData
        - direction : pyvista.PolyData
        - wheel_center_rear : pyvista.PolyData
        - spring_o : pyvista.PolyData
    """
    spring_o = simple_tube(data["U_SPRING_MOUNT"], data["l_spring_mount"][index])
    coil = simple_spring(data["U_SPRING_MOUNT"], data["l_spring_mount"][index])
    return pv.MultiBlock([spring_o, coil])

def rear_suspension_new(data, index=None):
    """
    Creates a suspension system configuration with a spring.

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data.
    index : int
        Index of the current data point.

    Returns
    -------
    tuple
        A tuple containing:
        - upper_control_arm : pyvista.PolyData
        - lower_control_arm : pyvista.PolyData
        - direction : pyvista.PolyData
        - wheel_center_rear : pyvista.PolyData
        - spring_o : pyvista.PolyData
    """
    spring_o = simple_spring(data["spring_mount_left"][index], data["spring_mount_right"][index])
    bar_right = simple_tube(data["bar_right_lower"][index], data["bar_right_upper"][index])
    bar_left = simple_tube(data["bar_left_lower"][index], data["bar_left_upper"][index])
    rocked_left = rocked(data["ROCKED_PIVOT_LEFT"], data["spring_mount_left"][index], data["bar_left_upper"][index])
    rocked_right = rocked(data["ROCKED_PIVOT_RIGHT"], data["spring_mount_right"][index], data["bar_right_upper"][index])

    return spring_o, bar_right, bar_left, rocked_left, rocked_right

