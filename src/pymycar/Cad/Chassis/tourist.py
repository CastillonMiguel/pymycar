"""
Tourist
=======
"""

import pyvista as pv
import numpy as np

def model_A(front_axle_to_com=1645*0.5,
            rear_axle_to_com=1645*0.5,
            front_track=1645*0.5,
            rear_track=1645*0.5,
            com_height=600.0,
            roll=0,
            pitch=0,
            yaw=0,
            x=0,
            y=0,
            z=0) -> pv.MultiBlock:
    """
    Generate a 3D model of a vehicle chassis.
    
    .. code-block::
    
       #                 <---------- d2 --------->      
       #
       #                   -------------------------      
       #                   |                       |
       #          h2       |          *p1          |  
       #                   |                       | 
       #     ---------------                       | 
       # h1 |                 cog                  |
       #    |                  * (x,y,z)           |
       #    |                                      |
       #    ---------------------------------------
       #    <------------------ d1 ---------------> 
       #

    Parameters
    ----------
    front_axle_to_com : float, optional
        Distance from the front axle to the center of mass (CoM).
    rear_axle_to_com : float, optional
        Distance from the rear axle to the center of mass (CoM).
    front_track : float, optional
        Front track width.
    rear_track : float, optional
        Rear track width.
    com_height : float, optional
        Height of the center of mass (CoM).
    roll : float, optional
        Roll angle in radians.
    pitch : float, optional
        Pitch angle in radians.
    yaw : float, optional
        Yaw angle in radians.
    x : float, optional
        X-coordinate of the center of mass (CoM).
    y : float, optional
        Y-coordinate of the center of mass (CoM).
    z : float, optional
        Z-coordinate of the center of mass (CoM).

    Returns
    -------
    pv.MultiBlock
        MultiBlock containing the chassis, cabin, and rear wheel.

    Notes
    -----
    The model consists of a chassis, a cabin, and a rear wheel, all represented as 3D geometric shapes.
    """
    cog = np.array([x, y, z + com_height])
    
    wheelbase = front_axle_to_com + rear_axle_to_com
    d1 = 1.5 * wheelbase
    h1 = 0.3 * wheelbase

    d2 = 0.6 * d1
    h2 = 800

    wd = 200
    chassis = pv.Cube(center=cog, x_length=d1, y_length=2.0*front_track, z_length=h1)
    cabin = pv.Cube(center=(cog[0]-0.5*(d1-d2), 0.0, cog[2] + 0.5*h1 + 0.5*h2), x_length=d2, y_length=2.0*front_track, z_length=h2)
    wheel_back = pv.Cylinder(center=(cog[0]-d1*0.5 - 0.5*wd, 0.0, cog[2]+0.5*h1), direction=(1, 0, 0), height=wd, radius=400)

    # Combine the chassis and cabin using merge
    chassis = chassis.rotate_x(np.rad2deg(roll))
    chassis = chassis.rotate_y(np.rad2deg(pitch))
    chassis = chassis.rotate_z(np.rad2deg(yaw))

    cabin = cabin.rotate_x(np.rad2deg(roll))
    cabin = cabin.rotate_y(np.rad2deg(pitch))
    cabin = cabin.rotate_z(np.rad2deg(yaw))

    wheel_back = wheel_back.rotate_x(np.rad2deg(roll))
    wheel_back = wheel_back.rotate_y(np.rad2deg(pitch))
    wheel_back = wheel_back.rotate_z(np.rad2deg(yaw))

    cad = pv.MultiBlock([chassis, cabin, wheel_back])
    return cad
