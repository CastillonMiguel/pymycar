"""
Double Wishbone Visualization
=============================

This module provides utilities for visualizing a double wishbone suspension system
using PyVista. It includes functions to construct the CAD representation of the
system components such as control arms, wheel, springs, and other suspension parts.

"""

from pymycar.Cad.geometric_forms import control_arm, simple_tube, simple_sphere, spring, rocked, simple_spring, dashed_line

def whisbone_cad_base(data, index=None):
    """
    Generates the base components of the suspension system.

    .. code-block::

       #                        
       #                    \\\    
       #                    \-/  
       #             UCA_REAR* 
       #                    /
       #                   / 
       #   -----------    /
       #    |       |    /
       #    |       |   *----------*UCA_FRONT
       #    |       | uca_outer   /⁻\.
       #    |       |             ///
       #    |       |
       #    |   wheel_center
       #  *-.-.-*   |        tierod_outer
       # wheel_center_axis    *--------------------*TIEROD_INNER
       #    |       |
       #    |       |
       #    |       |       lca_outer
       #    |       |      *------------*LCA_REAR
       #   -----------     \           /⁻\.
       #                    \          ///
       #                     \.
       #                      *LCA_FRONT
       #                     /⁻\.
       #                     ///
       
    
    +-------------------+-------------------------------+
    | Name              | Description                   | 
    +===================+===============================+
    | UCA_FRONT         | upper control arm front       | 
    +-------------------+-------------------------------+
    | UCA_REAR          | upper control arm rear        | 
    +-------------------+-------------------------------+
    | LCA_FRONT         | lower control arm front       | 
    +-------------------+-------------------------------+
    | LCA_REAR          | lower control arm rear        | 
    +-------------------+-------------------------------+
    | TIEROD_INNER      | tierod inner                  | 
    +-------------------+-------------------------------+
    | uca_outer         | upper control arm outer       |
    +-------------------+-------------------------------+
    | lca_outer         | lower control arm outer       |  
    +-------------------+-------------------------------+
    | tierod_outer      | tierod outer                  |
    +-------------------+-------------------------------+
    | wheel_center      | center of the wheel           |
    +-------------------+-------------------------------+
    | wheel_center_axis | axis of the wheel             |
    +-------------------+-------------------------------+

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

    Examples
    --------
    Create a base double wishbone suspension visualization.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad.Car.double_whisbone import whisbone_cad_base

    Define the suspension geometry points.
    
    >>> data = {
    ...     "UCA_FRONT": np.array([586.7, -314.5, 199.9]),
    ...     "UCA_REAR": np.array([930.7, -230.2, 244.2]),
    ...     "LCA_FRONT": np.array([588.7, -384.2, 76.8]),
    ...     "LCA_REAR": np.array([938.2, -191.2, 62.7]),
    ...     "TIEROD_INNER": np.array([934.2, -192.1, 81.2]),
    ...     "uca_outer": [np.array([953.0, -474.2, 272.2])],
    ...     "lca_outer": [np.array([934.8, -514.7, 47.9])],
    ...     "tierod_outer": [np.array([1027.1, -513.7, 43.6])],
    ...     "wheel_center": [np.array([941.5, -580.2, 155.1])],
    ...     "wheel_center_axis": [np.array([941.5, -680.2, 155.1])]
    ... }

    Generate the CAD elements and a representation of the wheel.
    
    >>> upper_control_arm, lower_control_arm, direction, wheel_center, wheel_axis = whisbone_cad_base(data, 0)
    >>> wheel = pv.Cylinder(center=data["wheel_center"][0], direction=(0, 1, 0), height=50, radius=200)

    Initialize the plotter and add the generated meshes.

    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(upper_control_arm, color="blue")
    >>> plotter.add_mesh(lower_control_arm, color="pink")
    >>> plotter.add_mesh(direction, color="green")
    >>> plotter.add_mesh(wheel, color="black", opacity=0.5)
    >>> plotter.add_mesh(wheel_axis, color="gray", opacity=0.5)
    >>> for name, coord in data.items():
    ...     pts = coord[0] if isinstance(coord, list) else coord
    ...     plotter.add_mesh(pv.Sphere(radius=5, center=pts), color='red')
    ...     plotter.add_point_labels([pts], [name], point_size=20, font_size=30, text_color='black', always_visible=True)
    >>> plotter.show()
    """
    upper_control_arm = control_arm(data["UCA_FRONT"], data["UCA_REAR"], data["uca_outer"][index])
    lower_control_arm = control_arm(data["LCA_FRONT"], data["LCA_REAR"], data["lca_outer"][index])
    direction = simple_tube(data["TIEROD_INNER"], data["tierod_outer"][index])
    wheel_center = simple_sphere(data["wheel_center"][index], 10)
    wheel_axis = dashed_line(data["wheel_center"][index], data["wheel_center_axis"][index])
    return upper_control_arm, lower_control_arm, direction, wheel_center, wheel_axis


def whisbone_cad_configuration_1(data, index=None):
    """
    Creates a suspension system configuration with a spring.

    .. code-block::

       #                 
       #                    \\\    
       #                    \-/  
       #             UCA_REAR* 
       #                    /
       #                   / 
       #   -----------    /
       #    |       |    /
       #    |       |   *----------*UCA_FRONT
       #    |       | uca_outer   /⁻\.
       #    |       |             ///
       #    |       |
       #    |       |
       #    |       |        tierod_outer
       #    |       |       *--------------------*TIEROD_INNER
       #    |       |
       #    |       |
       #    |       |       lca_outer
       #    |       |      *------------*LCA_REAR
       #   -----------     \           /⁻\.
       #                    \          ///
       #                     \.
       #                      *LCA_FRONT
       #                     /⁻\.
       #                     ///
       
    
    +----------------+-------------------------------+
    | Name           | Description                   | 
    +================+===============================+
    | UCA_FRONT      | upper control arm front       | 
    +----------------+-------------------------------+
    | UCA_REAR       | upper control arm rear        | 
    +----------------+-------------------------------+
    | LCA_FRONT      | lower control arm front       | 
    +----------------+-------------------------------+
    | LCA_REAR       | lower control arm rear        | 
    +----------------+-------------------------------+
    | TIEROD_INNER   | tierod inner                  | 
    +----------------+-------------------------------+
    | uca_outer      | upper control arm outer       |
    +----------------+-------------------------------+
    | lca_outer      | lower control arm outer       |  
    +----------------+-------------------------------+
    | tierod_outer   | tierod outer                  |
    +----------------+-------------------------------+
    | U_SPRING_MOUNT | upper spring mount            |
    +----------------+-------------------------------+
    | l_spring_mount | lower spring mount            |
    +----------------+-------------------------------+

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

    Examples
    --------
    Create a base double wishbone suspension with a spring visualization.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad.Car.double_whisbone import whisbone_cad_configuration_1

    Define the suspension geometry points.

    >>> data = {
    ...     "UCA_FRONT": np.array([586.7, -314.5, 199.9]),
    ...     "UCA_REAR": np.array([930.7, -230.2, 244.2]),
    ...     "LCA_FRONT": np.array([588.7, -384.2, 76.8]),
    ...     "LCA_REAR": np.array([938.2, -191.2, 62.7]),
    ...     "TIEROD_INNER": np.array([934.2, -192.1, 81.2]),
    ...     "uca_outer": [np.array([953.0, -474.2, 272.2])],
    ...     "lca_outer": [np.array([934.8, -514.7, 47.9])],
    ...     "tierod_outer": [np.array([1027.1, -513.7, 43.6])],
    ...     "wheel_center": [np.array([941.5, -580.2, 155.1])],
    ...     "wheel_center_axis": [np.array([941.5, -680.2, 155.1])],
    ...     "U_SPRING_MOUNT": np.array([831.7, -278.7, 251.2]),
    ...     "l_spring_mount": [np.array([849.2, -419.1, 76.4])]
    ... }

    Generate the CAD elements and a representation of the wheel.

    >>> upper_control_arm, lower_control_arm, direction, wheel_center, wheel_axis, spring_o = whisbone_cad_configuration_1(data, 0)
    >>> wheel = pv.Cylinder(center=data["wheel_center"][0], direction=(0, 1, 0), height=50, radius=200)

    Initialize the plotter and add the generated meshes.

    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(upper_control_arm, color="blue")
    >>> plotter.add_mesh(lower_control_arm, color="pink")
    >>> plotter.add_mesh(direction, color="green")
    >>> plotter.add_mesh(wheel_center, color="black")
    >>> plotter.add_mesh(wheel_axis, color="gray", opacity=0.5)
    >>> plotter.add_mesh(spring_o, color="red")
    >>> plotter.add_mesh(wheel, color="black", opacity=0.5)
    >>> for name, coord in data.items():
    ...     pts = coord[0] if isinstance(coord, list) else coord
    ...     plotter.add_mesh(pv.Sphere(radius=5, center=pts), color='red')
    ...     plotter.add_point_labels([pts], [name], point_size=20, font_size=30, text_color='black', always_visible=True)
    >>> plotter.show()
    """
    upper_control_arm, lower_control_arm, direction, wheel_center, wheel_axis = whisbone_cad_base(data, index)
    spring_o = spring(data["U_SPRING_MOUNT"], data["l_spring_mount"][index])
    return upper_control_arm, lower_control_arm, direction, wheel_center, wheel_axis, spring_o  


def whisbone_cad_configuration_2(data, index=None):
    """
    Creates a suspension system configuration with a rocker, push rod, and spring.

    .. code-block::

       #                        
       #                    \\\    
       #                    \-/  
       #             UCA_REAR* 
       #                    /
       #                   / 
       #   -----------    /
       #    |       |    /
       #    |       |   *----------*UCA_FRONT
       #    |       | uca_outer   /⁻\.
       #    |       |             ///
       #    |       |
       #    |       |
       #    |       |        tierod_outer
       #    |       |       *--------------------*TIEROD_INNER
       #    |       |
       #    |       |
       #    |       |       lca_outer
       #    |       |      *------------*LCA_REAR
       #   -----------     \           /⁻\.
       #                    \          ///
       #                     \.
       #                      *LCA_FRONT
       #                     /⁻\.
       #                     ///
       

    +-------------------+-------------------------------+
    | Name              | Description                   | 
    +===================+===============================+
    | UCA_FRONT         | upper control arm front       | 
    +-------------------+-------------------------------+
    | UCA_REAR          | upper control arm rear        | 
    +-------------------+-------------------------------+
    | LCA_FRONT         | lower control arm front       | 
    +-------------------+-------------------------------+
    | LCA_REAR          | lower control arm rear        | 
    +-------------------+-------------------------------+
    | TIEROD_INNER      | tierod inner                  | 
    +-------------------+-------------------------------+
    | uca_outer         | upper control arm outer       |
    +-------------------+-------------------------------+
    | lca_outer         | lower control arm outer       |  
    +-------------------+-------------------------------+
    | tierod_outer      | tierod outer                  |
    +-------------------+-------------------------------+
    | ROCKED_PIVOT      | rocked pivot                  |
    +-------------------+-------------------------------+
    | ROCKED_PIVOT_AXIS | rocked pivot axis             |
    +-------------------+-------------------------------+
    | U_SPRING_MOUNT    | upper spring mount            |
    +-------------------+-------------------------------+
    | push_rod_outer    | push rod outer                |
    +-------------------+-------------------------------+
    | push_rod_inner    | push rod inner                |
    +-------------------+-------------------------------+
    | l_spring_mount    | lower spring mount            |
    +-------------------+-------------------------------+

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

    Examples
    --------
    Create a base double wishbone suspension with a rocker, push rod, and spring visualization.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad.Car.double_whisbone import whisbone_cad_configuration_2

    Define the suspension geometry points.

    >>> data = {
    ...     "UCA_FRONT": np.array([586.7, -314.5, 199.9]), 
    ...     "UCA_REAR":  np.array([930.7, -230.2, 244.2]),
    ...     "LCA_FRONT": np.array([588.7, -384.2, 76.8]),
    ...     "LCA_REAR": np.array([938.2, -191.2, 62.7]),
    ...     "TIEROD_INNER": np.array([934.2,  -192.1,  81.2]),
    ...     "ROCKED_PIVOT": np.array([901.0, -139.00, 399.0]),
    ...     "ROCKED_PIVOT_AXIS": np.array([941.0, -139.00, 399.0]),
    ...     "U_SPRING_MOUNT": np.array([901.0,  -29.50, 499.0]),
    ...     "uca_outer": [np.array([953.0, -474.2, 272.2])], 
    ...     "lca_outer": [np.array([934.8, -514.7, 47.9])], 
    ...     "tierod_outer": [np.array([1027.1, -513.7, 43.6])],
    ...     "wheel_center": [np.array([941.5, -580.2, 155.1])],
    ...     "wheel_center_axis": [np.array([941.5, -680.2, 155.1])],
    ...     "push_rod_outer": [np.array([901.0, -379.00, 250.0])],
    ...     "push_rod_inner": [np.array([901.0, -139.00, 441.0])],
    ...     "l_spring_mount": [np.array([901.0, -130.20, 451.0])]
    ... }

    Generate the CAD elements and a representation of the wheel.

    >>> upper_control_arm, lower_control_arm, direction, wheel_center, wheel_axis, spring_o, push_rod, rocked_o = whisbone_cad_configuration_2(data, 0)
    >>> wheel = pv.Cylinder(center=data["wheel_center"][0], direction=(0, 1, 0), height=50, radius=200)

    Initialize the plotter and add the generated meshes.

    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(upper_control_arm, color="blue")
    >>> plotter.add_mesh(lower_control_arm, color="pink")
    >>> plotter.add_mesh(direction, color="green")
    >>> plotter.add_mesh(wheel_center, color="black")
    >>> plotter.add_mesh(wheel_axis, color="gray", opacity=0.5)
    >>> plotter.add_mesh(spring_o, color="red")
    >>> plotter.add_mesh(push_rod, color="black")
    >>> plotter.add_mesh(rocked_o, color="yellow")
    >>> plotter.add_mesh(wheel, color="black", opacity=0.5)
    >>> for name, coord in data.items():
    ...     pts = coord[0] if isinstance(coord, list) else coord
    ...     plotter.add_mesh(pv.Sphere(radius=5, center=pts), color='red')
    ...     plotter.add_point_labels([pts], [name], point_size=20, font_size=30, text_color='black', always_visible=True)
    >>> plotter.show()
    """
    upper_control_arm, lower_control_arm, direction, wheel_center, wheel_axis = whisbone_cad_base(data, index)
    rocked_o = rocked(data["ROCKED_PIVOT"], data["l_spring_mount"][index], data["push_rod_inner"][index])
    push_rod = simple_tube(data["push_rod_inner"][index], data["push_rod_outer"][index])
    spring_o = simple_spring(data["U_SPRING_MOUNT"], data["l_spring_mount"][index])
    return upper_control_arm, lower_control_arm, direction, wheel_center, wheel_axis, spring_o, push_rod, rocked_o
