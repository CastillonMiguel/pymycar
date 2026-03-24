"""
Geometric Forms
===============

This module contains functions to generate and manipulate basic geometric forms using PyVista. These forms can be used for visualization and analysis in various engineering and physics simulations. The functions in this module provide simple representations of common mechanical components such as control arms, tubes, cylinders, spheres, springs, and other structures.

Each function creates geometric shapes by connecting specified points in 3D space, allowing users to model complex systems efficiently. These forms can be used to build assemblies or test various configurations, making them useful for mechanical simulations, 3D modeling, and CAD systems.

The generated shapes are returned as `pv.MultiBlock` objects, which allow for efficient handling and visualization of multiple geometric forms in a single structure.

These functions provide an easy way to generate basic geometric components for more complex 3D models.

"""

import pyvista as pv
import numpy as np

def control_arm(point_a, point_b, common_point, radius=10, resolution=100, n_sides=10):
    """
    Generate a control arm (V-shape structure).

    Parameters
    ----------
    point_a : array-like
        Coordinates of the first base point of the control arm.
    point_b : array-like
        Coordinates of the second base point of the control arm.
    common_point : array-like
        Coordinates of the common apex point of the control arm.
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
    The control arm is formed by two Tubes connecting the base points
    to the common apex point.

    Examples
    --------
    Create a control arm mapping between three coordinates and show it using PyVista.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad import control_arm
    >>> a = control_arm(np.array([586.7, -314.5, 199.9]), np.array([930.7, -230.2, 244.2]), np.array([953.0, -474.2, 272.2]), radius=10, resolution=100, n_sides=10)
    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(a, color='red', name="Control Arm")
    >>> plotter.add_title("Control Arm")
    >>> plotter.show()
    """
    e1 = pv.Tube(pointa=point_a, pointb=common_point, resolution=resolution, radius=radius, n_sides=n_sides)
    e2 = pv.Tube(pointa=point_b, pointb=common_point, resolution=resolution, radius=radius, n_sides=n_sides)
    return pv.MultiBlock([e1, e2])


def simple_tube(point_a, point_b, radius=5, resolution=100, n_sides=10):
    """
    Generate a simple tube.

    Parameters
    ----------
    point_a : array-like
        Coordinates of the first point of the tube.
    point_b : array-like
        Coordinates of the second point of the tube.
    radius : float, optional
        Radius of the Tube, by default 5.
    resolution : int, optional
        Resolution of the Tube, by default 100.
    n_sides : int, optional
        Number of sides of the Tube, by default 10.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing a Tube representing the simple tube.

    Notes
    -----
    The simple tube is formed by a single Tube connecting point_a and point_b.

    Examples
    --------
    Create a tube between two coordinates and show it using PyVista.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad import simple_tube
    >>> tube = simple_tube(np.array([934.2, -192.1, 81.2]), np.array([1027.1, -513.7, 43.6]), radius=10, resolution=100, n_sides=10)
    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(tube, color='blue', name="Tie Rod Tube")
    >>> plotter.add_title("Tie Rod Tube")
    >>> plotter.show()
    """
    e5 = pv.Tube(pointa=point_a, pointb=point_b, resolution=resolution, radius=radius, n_sides=n_sides)
    return pv.MultiBlock([e5])


def simple_cylinder(center, height, radius):
    """
    Generate a simple cylinder.

    Parameters
    ----------
    center : array-like
        Coordinates of the center of the cylinder.
    height : float
        Height of the cylinder.
    radius : float
        Radius of the cylinder.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing a Cylinder representing the simple cylinder.

    Notes
    -----
    The simple cylinder is a Cylinder centered at the specified point with the given height and radius.

    Examples
    --------
    Create a cylinder at a specific coordinate and show it using PyVista.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad import simple_cylinder
    >>> b = simple_cylinder(np.array([941.5, -580.2, 155.1]), height=10, radius=5)
    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(b, color='green', name="Wheel Center Cylinder")
    >>> plotter.add_title("Wheel Center Cylinder")
    >>> plotter.show()
    """
    wheel = pv.Cylinder(center=center, direction=(0, 1, 0), height=height, radius=radius)
    return pv.MultiBlock([wheel])

def cylinder_from_two_points(center, point_a, point_b, height, radius):
    """
    Create a PyVista cylinder whose direction is defined by two points.

    Parameters
    ----------
    center : array-like
        Cylinder center [x, y, z].
    point_a : array-like
        First point defining the direction.
    point_b : array-like
        Second point defining the direction.
    height : float
        Cylinder height.
    radius : float
        Cylinder radius.

    Returns
    -------
    pyvista.PolyData
        Cylinder mesh.
    """

    direction = point_b - point_a
    norm = np.linalg.norm(direction)
    if norm == 0:
        raise ValueError("point_a and point_b cannot be the same point (direction length is zero).")
    direction = direction / norm

    cylinder = pv.Cylinder(
        center=center,
        direction=direction,
        height=height,
        radius=radius
    )
    return pv.MultiBlock([cylinder])

def simple_sphere(center, radius):
    """
    Generate a simple sphere.

    Parameters
    ----------
    center : array-like
        Coordinates of the center of the sphere.
    radius : float
        Radius of the sphere.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing a Sphere representing the simple sphere.

    Notes
    -----
    The simple sphere is a Sphere centered at the specified point with the given radius.

    Examples
    --------
    Create a sphere at a specific coordinate and show it using PyVista.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad import simple_sphere
    >>> c = simple_sphere(np.array([941.5, -580.2, 155.1]), radius=10)
    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(c, color='yellow', name="Wheel Center Sphere")
    >>> plotter.add_title("Wheel Center Sphere")
    >>> plotter.show()
    """
    point_wheel_center = pv.Sphere(radius=radius, center=center, theta_resolution=30, phi_resolution=30)
    return pv.MultiBlock([point_wheel_center])


def spring(point_a, point_b, radius=5):
    """
    Generate a spring.

    Parameters
    ----------
    point_a : array-like
        Coordinates of the upper mounting point of the spring.
    point_b : array-like
        Coordinates of the lower mounting point of the spring.
    radius : float, optional
        Radius of the Spheres and the Tube, by default 10.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing two Spheres and a Tube representing the spring.

    Notes
    -----
    The spring is formed by two Spheres at the upper and lower mounting points
    and a Tube connecting them.

    Examples
    --------
    Create a spring structure mapping between two coordinates and show it using PyVista.

    >>> import numpy as np
    >>> import pyvista as pv
    >>> from pymycar.Cad import spring
    >>> d = spring(np.array([831.7, -278.7, 251.2]), np.array([849.2, -419.1, 76.4]), radius=10)
    >>> plotter = pv.Plotter()
    >>> plotter.add_mesh(d, color='purple', name="Spring")
    >>> plotter.add_title("Spring Structure")
    >>> plotter.show()
    """
    p1 = simple_sphere(point_a, radius)
    p2 = simple_sphere(point_b, radius)
    return pv.MultiBlock([p1, p2, simple_tube(point_a, point_b)])

def spring_old(point_a, point_b, radius=10, coil_radius=10, n_coils=1, n_points=1000):
    """
    Generate a spring.

    Parameters
    ----------
    point_a : array-like
        Coordinates of the upper mounting point of the spring.
    point_b : array-like
        Coordinates of the lower mounting point of the spring.
    radius : float, optional
        Radius of the Spheres, by default 10.
    coil_radius : float, optional
        Radius of the spring coil, by default 5.
    n_coils : int, optional
        Number of coils in the spring, by default 10.
    n_points : int, optional
        Number of points to represent the spring coil, by default 100.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing two Spheres and a Helix representing the spring.

    Notes
    -----
    The spring is formed by two Spheres at the upper and lower mounting points
    and a Helix representing the spring coil.
    """
    # Create spheres at the mounting points
    p1 = pv.Sphere(radius=radius, center=point_a)
    p2 = pv.Sphere(radius=radius, center=point_b)
    p3 = pv.Sphere(radius=radius, center=[0,0,0])
    
    # Calculate the direction and length of the spring
    direction = np.array(point_b) - np.array(point_a)
    length = np.linalg.norm(direction)
    if length == 0:
        raise ValueError("point_a and point_b cannot be the same point (zero length direction).")
    direction = direction.astype(float) / length
    
    # Calculate a perpendicular direction
    if np.allclose(direction, [0, 0, 1]):
        perpendicular = np.array([1, 0, 0])
    else:
        reference_vector = np.array([0, 0, 1])
        perpendicular = np.cross(direction, reference_vector)
        perpendicular /= np.linalg.norm(perpendicular)
    # Create a polygon to represent the cross-section of the spring coil
    profile = pv.Polygon(
        center = [0,0,0],
        radius = coil_radius,
        normal =perpendicular,
        n_sides=30,
    )

    # Create the helical shape using extrude_rotate
    angle = 360 * n_coils
    extruded = profile.extrude_rotate(
        resolution=n_points,
        translation=length,
        dradius=0.0,
        angle=angle,
        capping=True,
        rotation_axis=direction
    )

    return pv.MultiBlock([p1, p2, p3, extruded])

def rocked(pivot, point_a, point_b):
    """
    Generate a structure with tubes connecting various points.

    Parameters
    ----------
    pivot : array-like
        Coordinates of the central pivot point.
    point_a : array-like
        Coordinates of the first connecting point.
    point_b : array-like
        Coordinates of the second connecting point.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing three Tubes representing the structure.

    Notes
    -----
    The structure is formed by three Tubes connecting various points.

    """
    e1 = simple_tube(pivot, point_a)
    e2 = simple_tube(pivot, point_b)
    e3 = simple_tube(point_a, point_b)
    return pv.MultiBlock([e1, e2, e3])

def rectangle_U(base_a, base_b, point_a, point_b, radius=10, resolution=100, n_sides=10):
    """
    Generate a U-shaped rectangular control arm using three tubes.

    Parameters
    ----------
    base_a : array-like
        Coordinates of the first base point of the control arm.
    base_b : array-like
        Coordinates of the second base point of the control arm.
    point_a : array-like
        Coordinates of the extended point connecting to base_a.
    point_b : array-like
        Coordinates of the extended point connecting to base_b.
    radius : float, optional
        Radius of the tubes, by default 10.
    resolution : int, optional
        Resolution of the tubes, by default 100.
    n_sides : int, optional
        Number of sides of the tubes, by default 10.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing three tubes representing the U-shaped control arm.

    Notes
    -----
    The control arm is formed by two tubes connecting the base points
    to their respective extended points, and a third tube connecting the two extended points.
    This forms a U-shaped rectangular structure.
    """
    e1 = pv.Tube(pointa=base_a, pointb=point_a, resolution=resolution, radius=radius, n_sides=n_sides)
    e2 = pv.Tube(pointa=base_b, pointb=point_b, resolution=resolution, radius=radius, n_sides=n_sides)
    e3 = pv.Tube(pointa=point_a, pointb=point_b, resolution=resolution, radius=radius, n_sides=n_sides)
    return pv.MultiBlock([e1, e2, e3])
