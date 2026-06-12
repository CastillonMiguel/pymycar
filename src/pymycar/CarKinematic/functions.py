"""
Functions: Suspension Kinematic Analysis
========================================
   

"""

import numpy as np
from scipy.optimize import fsolve

def generate_wheel_center_heights(wheel_center_i, max_height_increase, max_height_decrease, height_step):
    """
    Generate a range of wheel center heights based on the initial height and specified ranges.

    Parameters:
    - wheel_center_i (numpy.ndarray): Initial wheel center position [x, y, z].
    - max_height_increase (float): Maximum absolute height increase from the initial position.
    - max_height_decrease (float): Maximum absolute height decrease from the initial position.
    - height_step (float): Increment step for height adjustments.

    Returns:
    - wheel_center_heights (numpy.ndarray): Array of wheel center heights.
    - initial_height_index (int): Index of the initial height in the resulting array.

    Example:
    >>> import numpy as np
    >>> # Initial wheel center position [x, y, z]
    >>> wheel_center_i = np.array([0, 10, 0])
    >>> # Absolute maximum height increase and decrease
    >>> max_height_increase = 2.0
    >>> max_height_decrease = 1.0
    >>> # Increment step for height adjustments
    >>> height_step = 0.5
    >>> # Generate wheel center heights
    >>> wheel_center_heights, initial_height_index = generate_wheel_center_heights(wheel_center_i, max_height_increase, max_height_decrease, height_step)
    >>> print("Wheel Center Heights:", wheel_center_heights)
    >>> print("Initial Height Index:", initial_height_index)
    Wheel Center Heights: [ 9.   9.5 10.  10.5 11. ]
    Initial Height Index: 2
    """
    
    # Calculate absolute maximum height values
    max_height_increase = abs(max_height_increase)
    max_height_decrease = abs(max_height_decrease)
    
    # Generate positive and negative height ranges
    positive_heights = np.arange(wheel_center_i[2], wheel_center_i[2] + max_height_increase + height_step, height_step)
    negative_heights = np.arange(wheel_center_i[2] - max_height_decrease, wheel_center_i[2], height_step)

    # Combine positive and negative ranges
    wheel_center_heights = np.concatenate([negative_heights, positive_heights])

    # Find the index of the initial height in the array
    initial_height_index = np.where(wheel_center_heights == wheel_center_i[2])[0]

    return wheel_center_heights, initial_height_index[0]


def solve(wheel, index, initial_guess, residual, jacobian=None):
    """
    Solves a system of nonlinear equations for a sequence of wheel positions using the fsolve algorithm.
    This function iteratively solves for the unknowns at each wheel position, first moving forward from the given index to the end of the wheel array, then backward from the index to the start. The solutions are stored in a 2D array.
    Parameters
    ----------
    wheel : array_like
        Array of wheel positions or values to iterate over.
    index : int
        Starting index in the wheel array for the forward and backward solution process.
    initial_guess : array_like
        Initial guess for the unknowns to be solved by `fsolve`.
    residual : callable
        Function that computes the residuals of the system of equations. Should have the signature `residual(x, wheel_center_z)`.
    jacobian : callable, optional
        Function that computes the Jacobian matrix of the system. Should have the signature `jacobian(x, wheel_center_z)`. Default is None.
    Returns
    -------
    solution_save : ndarray
        2D array of solutions for each wheel position. Each row corresponds to a wheel position, and each column to a solved variable.
    Notes
    -----
    - Uses `scipy.optimize.fsolve` for solving the nonlinear system.
    - The function modifies `initial_guess` during the process.
    - The function assumes that the length of `initial_guess` times 3 matches the number of variables to be solved for each wheel position.
    """
    solution_save = np.zeros([len(wheel), len(initial_guess)*3])

    for i in range(index, len(wheel)):
        wheel_center_z = wheel[i]
        initial_guess = fsolve(residual, 
                               initial_guess,
                               args=(wheel_center_z),
                               fprime=jacobian,
                               col_deriv=0,
                               xtol=1e-12,
                               maxfev=0,
                               band=None,
                               epsfcn=None,
                               diag=None)
        
        solution_save[i,:] = initial_guess
        
    initial_guess = solution_save[index, :]
    for j in range(index, -1, -1):
        wheel_center_z = wheel[j]
        initial_guess = fsolve(residual, initial_guess, args=(wheel_center_z), fprime=jacobian,col_deriv=0,
        xtol=1e-12,
        maxfev=0,
        band=None,
        epsfcn=None,
        diag=None)
        solution_save[j,:] = initial_guess
        
    return solution_save


# Displacement Functions 
#############################################################
def get_wheel_base(data, index=None):
    """
    Calculate the wheel base (longitudinal displacement) for a suspension system.

    The wheel base is the longitudinal displacement of the wheel center along the vehicle's X-axis,
    referenced to a given position (usually the static or initial position). It is positive when the
    displacement is forward.

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data. Must include the key "wheel_center" as an array
        of wheel center coordinates and "index_reference" as the reference index.
    index : int, optional
        Index to use as the reference position. If None, uses `data["index_reference"]`.

    Returns
    -------
    wheel_base : numpy.ndarray
        Array of wheel base values (float), representing the longitudinal displacement for each position.

    Notes
    -----
    The wheel base is calculated as the difference in the X-coordinate of the wheel center
    relative to the reference index.

    Examples
    --------
    >>> wheel_base = get_wheel_base(data)
    >>> print(wheel_base)
    [ 0.   10.   20.  ... ]
    """
    if index is None:
        index = data["index_reference"]
    wheel_base = -(data["wheel_center"][:,0] - data["wheel_center"][index][0])
    return wheel_base


def get_wheel_track(data, index=None):
    """
    Calculate the wheel track (lateral displacement) for a suspension system.

    The wheel track is the lateral displacement of the wheel center along the vehicle's Y-axis,
    referenced to a given position. It is positive when the displacement is outward.

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data. Must include the key "wheel_center" as an array
        of wheel center coordinates and "index_reference" as the reference index.
    index : int, optional
        Index to use as the reference position. If None, uses `data["index_reference"]`.

    Returns
    -------
    wheel_track : numpy.ndarray
        Array of wheel track values (float), representing the lateral displacement for each position.

    Notes
    -----
    The wheel track is calculated as the difference in the Y-coordinate of the wheel center
    relative to the reference index.

    Examples
    --------
    >>> wheel_track = get_wheel_track(data)
    >>> print(wheel_track)
    [ 0.   -5.   -10.  ... ]
    """
    if index is None:
        index = data["index_reference"]
    wheel_track = -(data["wheel_center"][:,1] - data["wheel_center"][data["index_reference"]][1])
    return wheel_track


def get_wheel_jounce(data, index=None):
    """
    Calculate the wheel jounce (vertical displacement) for a suspension system.

    The wheel jounce is the vertical displacement of the wheel center along the vehicle's Z-axis,
    referenced to a given position. It is positive when the displacement is upward.

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data. Must include the key "wheel_center" as an array
        of wheel center coordinates and "index_reference" as the reference index.
    index : int, optional
        Index to use as the reference position. If None, uses `data["index_reference"]`.

    Returns
    -------
    wheel_jounce : numpy.ndarray
        Array of wheel jounce values (float), representing the vertical displacement for each position.

    Notes
    -----
    The wheel jounce is calculated as the difference in the Z-coordinate of the wheel center
    relative to the reference index.

    Examples
    --------
    >>> wheel_jounce = get_wheel_jounce(data)
    >>> print(wheel_jounce)
    [ 0.   2.   4.  ... ]
    """
    if index is None:
        index = data["index_reference"]
    wheel_jounce = data["wheel_center"][:,2] - data["wheel_center"][index][2]
    return wheel_jounce


# Rotation Functions 
#############################################################
# v1 = P2−P1
# v2 = P3−P2 
# v3 = P4−P3 

from scipy.spatial.transform import Rotation

def rotm2eul(rotm, order='ZYX'):
    """
    Converts a rotation matrix to Euler angles.
    
    Parameters:
        rotm (array-like): 3x3 rotation matrix.
        order (str): Order of the Euler angles (default is 'ZYX').
        
    Returns:
        eul (array): Euler angles in radians.
    """
    rotation = Rotation.from_matrix(rotm)  # Convert the rotation matrix to a Rotation object
    eul = rotation.as_euler(order, degrees=False)  # Get Euler angles in the specified order
    return eul


def wheel_angles(solution, index=None, degrees=False):
    
    a = solution["uca_outer"]
    b = solution["lca_outer"]
    c = solution["tierod_outer"]
    d = solution["wheel_center"]

    if index is None:
        index = solution["index_reference"]

    v1 = b - a
    v2 = c - a
    v3 = d - a

    v1c = b[index] - a[index]
    v2c = c[index] - a[index]
    v3c = d[index] - a[index]

    Xc = np.array([v1c, v2c, v3c]).T

    X_c_pseudo_inv = np.linalg.pinv(Xc)  # Use pinv for general case

    # Loop through each row of the matrices and compute the rotation matrix
    euler_angles = np.zeros([len(v1),3])

    for i in range(v1.shape[0]):
        
        # Stack the current vectors for this row into a matrix
        X = np.array([v1[i], v2[i], v3[i]]).T  # Shape (3, 3)

        R_matrix = X @ X_c_pseudo_inv

        # Convert rotation matrix to Euler angles
        rotation = Rotation.from_matrix(R_matrix)  # Convert the rotation matrix to a Rotation object
        euler_angles[i, :] = rotation.as_euler('ZYX', degrees=degrees)  # Get Euler angles in the specified order
    
    camber_angle = euler_angles[:,2]
    side_view_angle = euler_angles[:,1]
    toe_angle = -euler_angles[:,0]
    return toe_angle, side_view_angle, camber_angle
    
    
 
def get_caster_angle(data, index=None):
    """
    Calculate the caster angle for a suspension system.

    Parameters:
    - Suspension (object): Suspension object containing UCA and LCA data.

    Returns:
    - caster_angle (numpy.ndarray): Array of caster angle values (in radians).
    """
    if index is None:
        index = data["index_reference"]
    caster_angle = np.arctan((data["uca_outer"][:,0] - data["lca_outer"][:,0]) /
                             (data["uca_outer"][:,2] - data["lca_outer"][:,2]))
    return caster_angle


def get_kingpin_angle(data, index=None):
    """
    Calculate the kingpin angle for a suspension system.

    Parameters:
    - S1 (object): Suspension object containing UCA and LCA data.

    Returns:
    - kingpin_angle (numpy.ndarray): Array of kingpin angle values (in radians).
    """
    if index is None:
        index = data["index_reference"]
    kingpin_angle = np.arctan((data["uca_outer"][:,1] - data["lca_outer"][:,1]) /
                              (data["uca_outer"][:,2] - data["lca_outer"][:,2]))
    return kingpin_angle



    
def get_deflection(data, index=None):
    if index is None:
        index = data["index_reference"]
        
    l0 = np.linalg.norm(data["l_spring_mount"][index]- data["U_SPRING_MOUNT"])
    
    deflection = -( np.linalg.norm(data["l_spring_mount"]-data["U_SPRING_MOUNT"],axis=1) - l0)
    return deflection

def get_suspension_ratio(data, index=None):
    """
    Calculate the installation ratio (suspension ratio) for a suspension system.

    The installation ratio (λ) is the ratio between the vertical movement of the wheel and the movement
    produced in the spring/damper. It is calculated as the numerical derivative of the spring length
    with respect to the wheel jounce.

    Parameters
    ----------
    data : dict
        Dictionary containing suspension geometry data. Must include keys "l_spring_mount", "U_SPRING_MOUNT",
        and "index_reference".
    index : int, optional
        Index to use as the reference position. If None, uses `data["index_reference"]`.

    Returns
    -------
    ratio : numpy.ndarray
        Array of installation ratio values (float) for each position.

    Notes
    -----
    The installation ratio is defined as:

        λ = d_wheel / d_spring

    where d_wheel is the vertical displacement of the wheel (jounce) and d_spring is the displacement
    of the spring/damper. This ratio is used to compute equivalent vertical stiffness and damping.

    Examples
    --------
    >>> ratio = get_suspension_ratio(data)
    >>> print(ratio)
    [ 0.95  0.96  0.97 ... ]
    """
    if index is None:
        index = data["index_reference"]
        
    #deflection = get_deflection(data, index=index)
    jounce = get_wheel_jounce(data, index=index)
    ratio = abs(np.diff(np.linalg.norm(data["l_spring_mount"]-data["U_SPRING_MOUNT"],axis=1)))/abs(np.diff(jounce))

    return ratio
    
    
def get_geometric_suspension(data, index=None):
    
    if index is None:
        index = data["index_reference"]
    
    caster_angle = get_caster_angle(data, index)
    kingpin_angle = get_kingpin_angle(data, index)
    
    parameters ={
        "caster_angle": caster_angle,
        "kingpin_angle": kingpin_angle,
    }
    return parameters

        
def get_wheel(data, index=None):
    
    if index is None:
        index = data["index_reference"]
    
    # Displacement
    wheel_base = get_wheel_base(data, index)
    wheel_track = get_wheel_track(data, index)
    wheel_jounce = get_wheel_jounce(data, index)
    
    # Rotation
    toe_angle, side_view_angle, camber_angle = wheel_angles(data, index)
    
    caster_angle = get_caster_angle(data, index)
    kingpin_angle = get_kingpin_angle(data, index)
    wheel = {
        "wheel_base": wheel_base,
        "wheel_track": wheel_track,
        "wheel_jounce": wheel_jounce,
        "toe_angle": toe_angle,
        "side_view_angle": side_view_angle,
        "camber_angle": camber_angle,
        "caster_angle": caster_angle,
        "kingpin_angle": kingpin_angle,
    }
    return wheel
