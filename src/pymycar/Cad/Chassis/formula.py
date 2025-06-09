"""
Formula
=======
"""

import pyvista as pv
import numpy as np

def model_A(front_axle_to_com=1500,
            rear_axle_to_com=1645*0.5,
            front_track=1500*0.5,
            rear_track=1645*0.5,
            com_height=400.0,
            roll=0,
            pitch=0,
            yaw=0,
            x=0,
            y=0,
            z=0) -> pv.MultiBlock:
    """
    Generate a 3D model of a Formula vehicle chassis.

    .. code-block::
    
       #                                                 ---
       #---------------------------                      | |
       #                            |                      | |
       #                            ------------          | |
       #                                        |          | |
       #-----------   CoG               A      ----B-----|C|
       #            |    *                *          *     |*|
       #-----------                            ----------| |
       #                                        |          | |
       #                            ------------          | |
       #                            |                      | |
       #---------------------------                      | |
       #                                                 ---
                                                    
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
        MultiBlock containing the chassis components.

    Notes
    -----
    The model consists of multiple boxes representing different parts of the vehicle chassis.
    """
    cog = np.array([x, y, z + com_height])
    lf = front_track
    lr = front_track

    t1 = 1000
    t2 = 1000
    t3 = 1000
    t4 = 1000

    front_axle_to_com *= 0.8 
    d_CoG_A = front_axle_to_com
    d_A_B = front_axle_to_com * 0.5
    d_B_C = front_axle_to_com / 3.0

    box1_x, box1_y, box1_z = 2 * front_axle_to_com, front_track * 2, 400
    box2_x, box2_y, box2_z = 0.33 * 2 * front_axle_to_com, 0.53 * front_track * 2, 300
    box3_x, box3_y, box3_z = 0.26 * 2 * front_axle_to_com, 0.2 * front_track * 2, 200
    box4_x, box4_y, box4_z = 0.066 * 2 * front_axle_to_com, 1.333 * front_track * 2, 50
    box5_x, box5_y, box5_z = 0.5 * 2 * front_axle_to_com, 0.1333 * front_track * 2, 600
    box6_x, box6_y, box6_z = 0.133 * 2 * front_axle_to_com, 1.333 * front_track * 2, 200

    PA = np.array([cog[0] + box1_x * 0.5 + box2_x * 0.5, 0.0, box3_z + 0.25 * box2_z])
    PB = np.array([PA[0] + box2_x * 0.5 + box3_x * 0.5, 0.0, 0.5 * box3_z])
    PC = np.array([PB[0] + box3_x * 0.5 + box4_x * 0.5, 0.0, 0.5 * box4_z])
    PD = np.array([cog[0] - box5_x * 0.5, 0.0, box1_z + 0.5 * box5_z])
    PE = np.array([PD[0] - box5_x * 0.5 - box6_x * 0.7, 0.0, PD[2] + 0.5 * box6_z])

    axe_front_front = 1225
    wing_length = 250

    BOX1 = pv.Cube(center=cog, x_length=box1_x, y_length=box1_y, z_length=box1_z)
    BOX2 = pv.Cube(center=PA, x_length=box2_x, y_length=box2_y, z_length=box2_z)
    BOX3 = pv.Cube(center=PB, x_length=box3_x, y_length=box3_y, z_length=box3_z)
    BOX4 = pv.Cube(center=PC, x_length=box4_x, y_length=box4_y, z_length=box4_z)
    BOX5 = pv.Cube(center=PD, x_length=box5_x, y_length=box5_y, z_length=box5_z)
    BOX6 = pv.Cube(center=PE, x_length=box6_x, y_length=box6_y, z_length=box6_z)

    cad = pv.MultiBlock([BOX1, BOX2, BOX3, BOX4, BOX5, BOX6])
    return cad

def model_B(front_axle_to_com=1500,
            rear_axle_to_com=1645*0.5,
            front_track=1500*0.5,
            rear_track=1645*0.5,
            com_height=400.0,
            roll=0,
            pitch=0,
            yaw=0,
            x=0,
            y=0,
            z=0) -> pv.MultiBlock:
    """
    Generate a 3D model of a different Formula vehicle chassis.

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
        MultiBlock containing the chassis components.

    Notes
    -----
    The model consists of multiple boxes representing different parts of the vehicle chassis.
    """
    wheelbase = rear_axle_to_com + front_axle_to_com
    h = 400 / 4800 * wheelbase
    box1_x, box1_y, box1_z = 0.7 * wheelbase, front_track, h
    box2_x, box2_y, box2_z = 0.5 * front_axle_to_com, 800 / 1500 * front_track, 300 / 400 * h
    box3_x, box3_y, box3_z = 0.25 * front_axle_to_com, 300 / 1500 * front_track, 200 / 400 * h
    box4_x, box4_y, box4_z = 0.05 * front_axle_to_com, 2000 / 1500 * front_track, 50 / 400 * h
    box5_x, box5_y, box5_z = 0.5 * 0.7 * wheelbase, 200 / 1500 * front_track, 600 / 400 * h
    box6_x, box6_y, box6_z = 0.1 * front_axle_to_com, 2000 / 1500 * front_track, 200 / 400 * h

    cog = np.array([x, y, box1_z])
    PA = np.array([cog[0] + box1_x * 0.5 + box2_x * 0.5, cog[1], box3_z + 0.25 * box2_z])
    PB = np.array([PA[0] + box2_x * 0.5 + box3_x * 0.5, cog[1], 0.5 * box3_z])
    PC = np.array([PB[0] + box3_x * 0.5 + box4_x * 0.5, cog[1], 0.5 * box4_z])
    PD = np.array([cog[0] - box5_x * 0.5, cog[1], box1_z + 0.5 * box5_z])
    PE = np.array([PD[0] - box5_x * 0.5 - box6_x * 0.7, cog[1], PD[2] + 0.5 * box6_z])

    BOX1 = pv.Cube(center=cog, x_length=box1_x, y_length=box1_y, z_length=box1_z)
    BOX2 = pv.Cube(center=PA, x_length=box2_x, y_length=box2_y, z_length=box2_z)
    BOX3 = pv.Cube(center=PB, x_length=box3_x, y_length=box3_y, z_length=box3_z)
    BOX4 = pv.Cube(center=PC, x_length=box4_x, y_length=box4_y, z_length=box4_z)
    BOX5 = pv.Cube(center=PD, x_length=box5_x, y_length=box5_y, z_length=box5_z)
    BOX6 = pv.Cube(center=PE, x_length=box6_x, y_length=box6_y, z_length=box6_z)

    halo1 = pv.Cylinder(center=(-2400, 1000, 0.0), direction=(0, 0, 1), height=500, radius=100)

    cad = pv.MultiBlock([BOX1, BOX2, BOX3, BOX4, BOX5, BOX6])
    return cad