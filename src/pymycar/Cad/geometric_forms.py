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

def control_arm(uca_front, uca_rear, uca_outer_i, radius=10, resolution=100, n_sides=10):
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
    e1 = pv.Tube(uca_front, uca_outer_i, resolution, radius, n_sides)
    e2 = pv.Tube(uca_rear, uca_outer_i, resolution, radius, n_sides)
    return pv.MultiBlock([e1, e2])


def simple_tube(tierod_inner, tierod_outer_i, radius=5, resolution=100, n_sides=10):
    """
    Generate a simple tube.

    Parameters
    ----------
    tierod_inner : array-like
        Coordinates of the inner point of the tube.
    tierod_outer_i : array-like
        Coordinates of the outer point of the tube.
    radius : float, optional
        Radius of the Tube, by default 10.
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
    The simple tube is formed by a single Tube connecting the inner and outer points.

    """
    e5 = pv.Tube(tierod_inner, tierod_outer_i, resolution, radius, n_sides)
    return pv.MultiBlock([e5])


def simple_cylinder(wheel_center_i, height, radius):
    """
    Generate a simple cylinder.

    Parameters
    ----------
    wheel_center_i : array-like
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

    """
    wheel = pv.Cylinder(center=wheel_center_i, direction=(0, 1, 0), height=height, radius=radius)
    return pv.MultiBlock([wheel])


def simple_sphere(wheel_center_i, radius):
    """
    Generate a simple sphere.

    Parameters
    ----------
    wheel_center_i : array-like
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

    """
    point_wheel_center = pv.Sphere(radius, wheel_center_i, theta_resolution=30, phi_resolution=30)
    return pv.MultiBlock([point_wheel_center])


def spring(u_spring_mount, l_spring_mount_i, radius=5):
    """
    Generate a spring.

    Parameters
    ----------
    u_spring_mount : array-like
        Coordinates of the upper mounting point of the spring.
    l_spring_mount_i : array-like
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

    """
    p1 = simple_sphere(u_spring_mount, radius)
    p2 = simple_sphere(l_spring_mount_i, radius)
    return pv.MultiBlock([p1, p2, simple_tube(u_spring_mount, l_spring_mount_i)])

def spring_old(u_spring_mount, l_spring_mount, radius=10, coil_radius=10, n_coils=1, n_points=1000):
    """
    Generate a spring.

    Parameters
    ----------
    u_spring_mount : array-like
        Coordinates of the upper mounting point of the spring.
    l_spring_mount : array-like
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
    p1 = pv.Sphere(radius=radius, center=u_spring_mount)
    p2 = pv.Sphere(radius=radius, center=l_spring_mount)
    p3 = pv.Sphere(radius=radius, center=[0,0,0])
    
    # Calculate the direction and length of the spring
    direction = l_spring_mount - u_spring_mount
    direction = direction[0]
    length = np.linalg.norm(direction)
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

    return pv.MultiBlock([p1, p3, extruded])

def rocked(rocked_pivot, l_spring_mount, push_rod_inner_i):
    """
    Generate a structure with tubes connecting various points.

    Parameters
    ----------
    rocked_pivot : array-like
        Coordinates of the rocked pivot point.
    l_spring_mount : array-like
        Coordinates of the lower mounting point of the spring.
    push_rod_inner_i : array-like
        Coordinates of the inner point of the push rod.

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing three Tubes representing the structure.

    Notes
    -----
    The structure is formed by three Tubes connecting various points.

    """
    e1 = simple_tube(rocked_pivot, l_spring_mount)
    e2 = simple_tube(rocked_pivot, push_rod_inner_i)
    e3 = simple_tube(l_spring_mount, push_rod_inner_i)
    return pv.MultiBlock([e1, e2, e3])
