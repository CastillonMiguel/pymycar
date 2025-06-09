"""
Double Wishbone Visualization
=============================

This module provides utilities for visualizing a double wishbone suspension system
using PyVista. It includes functions to construct the CAD representation of the
system components such as control arms, wheel, springs, and other suspension parts.

"""

from pymycar.Cad.geometric_forms import control_arm, simple_tube, simple_sphere, spring, rocked

def whisbone_cad_base(data, index=None):
    """
    Generates the base components of the suspension system.

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
        - wheel_center : pyvista.PolyData
    """
    upper_control_arm = control_arm(data["UCA_FRONT"], data["UCA_REAR"], data["uca_outer"][index])
    lower_control_arm = control_arm(data["LCA_FRONT"], data["LCA_REAR"], data["lca_outer"][index])
    direction = simple_tube(data["TIEROD_INNER"], data["tierod_outer"][index])
    wheel_center = simple_sphere(data["wheel_center"][index], 10)
    return upper_control_arm, lower_control_arm, direction, wheel_center


def whisbone_cad_configuration_1(data, index=None):
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
        - wheel_center : pyvista.PolyData
        - spring_o : pyvista.PolyData
    """
    upper_control_arm, lower_control_arm, direction, wheel_center = whisbone_cad_base(data, index)
    spring_o = spring(data["U_SPRING_MOUNT"], data["l_spring_mount"][index])
    return upper_control_arm, lower_control_arm, direction, wheel_center, spring_o  


def whisbone_cad_configuration_2(data, index=None):
    """
    Creates a suspension system configuration with a rocker, push rod, and spring.

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
        - wheel_center : pyvista.PolyData
        - spring_o : pyvista.PolyData
        - push_rod : pyvista.PolyData
        - rocked_o : pyvista.PolyData
    """
    upper_control_arm, lower_control_arm, direction, wheel_center = whisbone_cad_base(data, index)
    rocked_o = rocked(data["ROCKED_PIVOT"], data["l_spring_mount"][index], data["push_rod_inner"][index])
    push_rod = simple_tube(data["push_rod_inner"][index], data["push_rod_outer"][index])
    spring_o = spring(data["U_SPRING_MOUNT"], data["l_spring_mount"][index])
    return upper_control_arm, lower_control_arm, direction, wheel_center, spring_o, push_rod, rocked_o
