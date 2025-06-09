"""
Multilink Visualization
=======================

This module provides utilities for visualizing a double wishbone suspension system
using PyVista. It includes functions to construct the CAD representation of the
system components such as control arms, wheel, springs, and other suspension parts.

"""

from pymycar.Cad.geometric_forms import simple_tube, simple_sphere, spring

def multilink_cad_base(data, index=None):
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
    upper_control_arm = simple_tube(data["UCA_FRONT"], data["uca_outer"][index])
    lower_control_arm = simple_tube(data["LCA_FRONT"], data["lca_outer"][index])
    
    upper_control_arm_aux = simple_tube(data["UCA_REAR"], data["uca_outer_aux"][index])
    lower_control_arm_aux = simple_tube(data["LCA_REAR"], data["lca_outer_aux"][index])
    
    direction = simple_tube(data["TIEROD_INNER"], data["tierod_outer"][index])
    wheel_center = simple_sphere(data["wheel_center"][index], 10)
    return upper_control_arm, lower_control_arm, upper_control_arm_aux, lower_control_arm_aux, direction, wheel_center


def multilink_cad_configuration_1(data, index=None):
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
    upper_control_arm, lower_control_arm, upper_control_arm_aux, lower_control_arm_aux, direction, wheel_center = multilink_cad_base(data, index)
    spring_o = spring(data["U_SPRING_MOUNT"], data["l_spring_mount"][index])
    return upper_control_arm, lower_control_arm, upper_control_arm_aux, lower_control_arm_aux, direction, wheel_center, spring_o
