"""
Motorbike Front Assembly Visualization
======================================

"""

import pyvista as pv
from pymycar.Cad.geometric_forms import rectangle_U, control_arm, simple_tube, simple_sphere, spring, rocked
from pymycar.Cad.geometric_forms import control_arm, simple_tube, simple_sphere, spring, rocked


###############################################################################
# Forks
# -----

def fork_front_suspension_steer(data, index=None):
    """
    Creates the CAD visualization for a front fork suspension.

    .. code-block::

        #
        #
        #    fork_left_upper *       
        #                    |    * STEERING_AXIS_TOP    
        #                    |     \                        
        #                    |      * STEERING_AXIS_BOTTOM                       
        #                    |                 
        #                    |         * fork_right_upper    
        #                    |         |                
        #   fork_left_middle *         | 
        #                    |         |
        #                    |         |
        #                    |         |
        #  fork_left_bottom  *         * fork_right_middle 
        #                      \       |  
        #                       \      |
        #           wheel_center *     |
        #                          \   |   
        #                            \ |
        #                              *fork_right_bottom
        #                     
        #         
        #

    +-------------------------+----------------------------------+--------+
    | Points Name             | Description                      | Type   |
    +=========================+==================================+========+
    | wheel_center            | Center of the Wheel              | mobile |
    +-------------------------+----------------------------------+--------+
    | STEERING_AXIS_TOP       | Steering axis top point          | fixed  |
    +-------------------------+----------------------------------+--------+
    | STEERING_AXIS_BOTTOM    | Steering axis bottom point       | fixed  |
    +-------------------------+----------------------------------+--------+
    | fork_right_upper        | Fork right upper attachment      | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_left_upper         | Fork left upper attachment       | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_right_middle       | Fork right middle attachment     | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_left_middle        | Fork left middle attachment      | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_right_bottom       | Fork right bottom attachment     | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_left_bottom        | Fork left bottom attachment      | mobile |
    +-------------------------+----------------------------------+--------+

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data points.
    index : int, optional
        Index of the current data point in the data arrays. Default is None.

    Returns
    -------
    tuple
        A tuple containing the following PyVista PolyData/MultiBlock objects:
        - bar_right_top : pyvista.PolyData
        - bar_left_top : pyvista.PolyData
        - U_form : pyvista.MultiBlock
        - steer_axis : pyvista.PolyData

    Examples
    --------
    Create a base double wishbone suspension visualization.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad.MotorCycle.front_assembly import fork_front_suspension
    
    Define the suspension geometry points.

    >>> data = {
    ...     "wheel_center": [np.array([1100.0,   0.0,     0.0])],
    ...     "STEERING_AXIS_TOP": np.array([900.0, 0.0, 600.0]),
    ...     "STEERING_AXIS_BOTTOM": np.array([1000.0, 0.0, 500.0]),
    ...     "fork_right_upper": [np.array([900.0, -200.0, 600.0])],
    ...     "fork_left_upper": [np.array([900.0, 200.0, 600.0])],
    ...     "fork_right_middle": [np.array([999.0, -200.0, 300.0])],
    ...     "fork_left_middle": [np.array([999.0, 200.0, 300.0])],
    ...     "fork_right_bottom": [np.array([1100.0, -200.0, 0.0])],
    ...     "fork_left_bottom": [np.array([1100.0, 200.0, 0.0])],
    ... }
    
    Generate the CAD elements and a representation of the wheel.

    >>> wheel = pv.Cylinder(center=data["wheel_center"][0], direction=(0, 1, 0), height=50, radius=200)
    >>> bar_right_top, bar_left_top, U_form, steer_axis = fork_front_suspension(data, 0)
    
    Initialize the plotter and add the generated meshes.

    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(wheel, color="black", opacity=1.0)
    >>> plotter.add_mesh(bar_right_top, color="red")
    >>> plotter.add_mesh(bar_left_top, color="red")
    >>> plotter.add_mesh(U_form, color="green")
    >>> plotter.add_mesh(steer_axis, color="blue")
    >>> for name, coord in data.items():
    ...     pts = coord[0] if isinstance(coord, list) else coord
    ...     plotter.add_mesh(pv.Sphere(radius=5, center=pts), color='red')
    ...     plotter.add_point_labels([pts], [name], point_size=20, font_size=30, text_color='black', always_visible=True)
    >>> plotter.show()
    """

    aux_1 = 0.5* ((data["fork_right_upper"][index]) + (data["fork_right_bottom"][index]))
    aux_2 =  0.5* ((data["fork_left_upper"][index]) +  (data["fork_left_bottom"][index]))
    
    aux_1_b = 0.5* ((data["fork_right_upper"][index]) + (data["fork_right_bottom"][index]))
    aux_2_b =  0.5* ((data["fork_left_upper"][index]) +  (data["fork_left_bottom"][index]))
    
    steer_axis = simple_tube(data["STEERING_AXIS_TOP"], data["STEERING_AXIS_BOTTOM"])
    bar_right = simple_tube(data["fork_right_upper"][index], data["STEERING_AXIS_BOTTOM"], radius=10, resolution=100, n_sides=10)
    bar_left = simple_tube(data["fork_left_upper"][index], data["STEERING_AXIS_BOTTOM"], radius=10, resolution=100, n_sides=10)

    U_form_top = rectangle_U(aux_1, aux_2, data["fork_right_upper"][index], data["fork_left_upper"][index], radius=10, resolution=100, n_sides=10)
    
    U_form_bottom = rectangle_U(aux_1_b, aux_2_b, data["fork_right_bottom"][index], data["fork_left_bottom"][index], radius=5, resolution=100, n_sides=10)

    return steer_axis, pv.MultiBlock([U_form_top, bar_right, bar_left]), U_form_bottom


def fork_front_suspension(data, index=None):
    """
    Creates the CAD visualization for a front fork suspension.

    .. code-block::

        #
        #
        #    fork_left_upper *       
        #                    |    * STEERING_AXIS_TOP    
        #                    |     \                        
        #                    |      * STEERING_AXIS_BOTTOM                       
        #                    |                 
        #                    |         * fork_right_upper    
        #                    |         |                
        #   fork_left_middle *         | 
        #                    |         |
        #                    |         |
        #                    |         |
        #  fork_left_bottom  *         * fork_right_middle 
        #                      \       |  
        #                       \      |
        #           wheel_center *     |
        #                          \   |   
        #                            \ |
        #                              *fork_right_bottom
        #                     
        #         
        #

    +-------------------------+----------------------------------+--------+
    | Points Name             | Description                      | Type   |
    +=========================+==================================+========+
    | wheel_center            | Center of the Wheel              | mobile |
    +-------------------------+----------------------------------+--------+
    | STEERING_AXIS_TOP       | Steering axis top point          | fixed  |
    +-------------------------+----------------------------------+--------+
    | STEERING_AXIS_BOTTOM    | Steering axis bottom point       | fixed  |
    +-------------------------+----------------------------------+--------+
    | fork_right_upper        | Fork right upper attachment      | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_left_upper         | Fork left upper attachment       | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_right_middle       | Fork right middle attachment     | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_left_middle        | Fork left middle attachment      | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_right_bottom       | Fork right bottom attachment     | mobile |
    +-------------------------+----------------------------------+--------+
    | fork_left_bottom        | Fork left bottom attachment      | mobile |
    +-------------------------+----------------------------------+--------+

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data points.
    index : int, optional
        Index of the current data point in the data arrays. Default is None.

    Returns
    -------
    tuple
        A tuple containing the following PyVista PolyData/MultiBlock objects:
        - bar_right_top : pyvista.PolyData
        - bar_left_top : pyvista.PolyData
        - U_form : pyvista.MultiBlock
        - steer_axis : pyvista.PolyData

    Examples
    --------
    Create a base double wishbone suspension visualization.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad.MotorCycle.front_assembly import fork_front_suspension
    
    Define the suspension geometry points.

    >>> data = {
    ...     "wheel_center": [np.array([1100.0,   0.0,     0.0])],
    ...     "STEERING_AXIS_TOP": np.array([900.0, 0.0, 600.0]),
    ...     "STEERING_AXIS_BOTTOM": np.array([1000.0, 0.0, 500.0]),
    ...     "fork_right_upper": [np.array([900.0, -200.0, 600.0])],
    ...     "fork_left_upper": [np.array([900.0, 200.0, 600.0])],
    ...     "fork_right_middle": [np.array([999.0, -200.0, 300.0])],
    ...     "fork_left_middle": [np.array([999.0, 200.0, 300.0])],
    ...     "fork_right_bottom": [np.array([1100.0, -200.0, 0.0])],
    ...     "fork_left_bottom": [np.array([1100.0, 200.0, 0.0])],
    ... }
    
    Generate the CAD elements and a representation of the wheel.

    >>> wheel = pv.Cylinder(center=data["wheel_center"][0], direction=(0, 1, 0), height=50, radius=200)
    >>> bar_right_top, bar_left_top, U_form, steer_axis = fork_front_suspension(data, 0)
    
    Initialize the plotter and add the generated meshes.

    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(wheel, color="black", opacity=1.0)
    >>> plotter.add_mesh(bar_right_top, color="red")
    >>> plotter.add_mesh(bar_left_top, color="red")
    >>> plotter.add_mesh(U_form, color="green")
    >>> plotter.add_mesh(steer_axis, color="blue")
    >>> for name, coord in data.items():
    ...     pts = coord[0] if isinstance(coord, list) else coord
    ...     plotter.add_mesh(pv.Sphere(radius=5, center=pts), color='red')
    ...     plotter.add_point_labels([pts], [name], point_size=20, font_size=30, text_color='black', always_visible=True)
    >>> plotter.show()
    """

    data["fork_right_middle"] = (data["fork_right_upper"] + data["fork_right_bottom"]) / 2
    data["fork_left_middle"] = (data["fork_left_upper"] + data["fork_left_bottom"]) / 2

    data["fork_right_middle_b"] = (data["fork_right_upper"] + data["fork_right_bottom"]) / 2
    data["fork_left_middle_b"] = (data["fork_left_upper"] + data["fork_left_bottom"]) / 2

    # bar_right_top = simple_tube(data["fork_right_upper"][index], data["fork_right_middle"][index])
    # bar_left_top = simple_tube(data["fork_left_upper"][index], data["fork_left_middle"][index])
    # U_form = rectangle_U(data["fork_right_middle"][index], data["fork_left_middle"][index], data["fork_right_bottom"][index], data["fork_left_bottom"][index], radius=10, resolution=100, n_sides=10)
    # steer_axis = simple_tube(data["STEERING_AXIS_TOP"], data["STEERING_AXIS_BOTTOM"])
    # return bar_right_top, bar_left_top, U_form, steer_axis

    steer_axis = simple_tube(data["STEERING_AXIS_TOP"], data["STEERING_AXIS_BOTTOM"])
    bar_right = simple_tube(data["fork_right_upper"][index], data["STEERING_AXIS_BOTTOM"], radius=10, resolution=100, n_sides=10)
    bar_left = simple_tube(data["fork_left_upper"][index], data["STEERING_AXIS_BOTTOM"], radius=10, resolution=100, n_sides=10)

    U_form_top = rectangle_U(data["fork_right_middle"][index], data["fork_left_middle"][index], data["fork_right_upper"][index], data["fork_left_upper"][index], radius=10, resolution=100, n_sides=10)
    
    U_form_bottom = rectangle_U(data["fork_right_middle_b"][index], data["fork_left_middle_b"][index], data["fork_right_bottom"][index], data["fork_left_bottom"][index], radius=5, resolution=100, n_sides=10)

    return steer_axis, pv.MultiBlock([U_form_top, bar_right, bar_left]), U_form_bottom
    