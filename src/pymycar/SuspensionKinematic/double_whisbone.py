"""
Suspension: Double Wishbone
===========================

This module provides functions to analyze and simulate the behavior of a double wishbone suspension system. The double wishbone suspension is a type of vehicle suspension design that uses two wishbone-shaped arms (or control arms) to locate the wheel. This type of suspension is widely used in various vehicles, from road cars to competition vehicles.

"""

###############################################################################
# Import necessary libraries
# --------------------------
import os
import numpy as np


###############################################################################
# Import from pymycar package
# ---------------------------
from pymycar.files import prepare_simulation, save_results_2_txt
from pymycar.Logger.library_versions import logger_suspension_kinematics
from pymycar.SuspensionKinematic.functions import solve, generate_wheel_center_heights
from pymycar.SuspensionKinematic.suspension_files import saved_defined_geometry # save_data
from pymycar.SuspensionKinematic.functions import get_wheel

def double_whisbone_base(data, max_height_increase, max_height_decrease, height_step, save_to_txt=True, result_folder_name="results", path = None):
    """
    Computes and solves the geometric constraints for a double wishbone suspension system.

    The function generates different wheel center heights based on input constraints, then calculates
    the residuals for a non-linear optimization problem to find the correct configuration of the
    suspension system.

    Parameters
    ----------
    data : dict
        A dictionary containing the initial measurements and reference points for the suspension system.
        Expected keys include:
            - 'wheel_center': The initial wheel center position.
            - 'uca_outer': The outer UCA (Upper Control Arm) position.
            - 'UCA_FRONT': The front reference point for the UCA.
            - 'UCA_REAR': The rear reference point for the UCA.
            - 'lca_outer': The outer LCA (Lower Control Arm) position.
            - 'LCA_FRONT': The front reference point for the LCA.
            - 'LCA_REAR': The rear reference point for the LCA.
            - 'tierod_outer': The outer tierod position.
            - 'TIEROD_INNER': The inner reference point for the tierod.
    max_height_increase : float
        Maximum increase in wheel center height for the analysis.
    max_height_decrease : float
        Maximum decrease in wheel center height for the analysis.
    height_step : float
        Step size for incrementing and decrementing the wheel center height.
    save_to_txt : bool, optional
        If True, the results will be saved to a text file. Default is True.
    result_folder_name : str, optional
        The name of the folder where results will be saved. Default is "results".
    path : str, optional
        The path where the results folder will be created. If None, the current working directory is used. Default is None.

    Returns
    -------
    solution : dict
        A dictionary with the optimized suspension parameters and their values:
            - 'UCA_FRONT': The front UCA position.
            - 'UCA_REAR': The rear UCA position.
            - 'LCA_FRONT': The front LCA position.
            - 'LCA_REAR': The rear LCA position.
            - 'TIEROD_INNER': The inner tierod position.
            - 'uca_outer': Optimized outer UCA positions.
            - 'lca_outer': Optimized outer LCA positions.
            - 'tierod_outer': Optimized outer tierod positions.
            - 'wheel_center': Optimized wheel center positions.
            - 'index_reference': Index reference for the wheel center heights.

    Notes
    -----
    The function utilizes an optimization algorithm to solve for the configuration of the suspension
    system that satisfies the geometric constraints. The geometric model assumes a double wishbone
    suspension layout with specific reference points for each component.

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
       #    |       | uca_outer   /⁻\ 
       #    |       |             ///
       #    |       |
       #    |  wheel center
       #    |   *   |        tierod_outer
       #    |       |       *--------------------*TIEROD_INNER
       #    |       |
       #    |       |
       #    |       |       lca_outer
       #    |       |      *------------*LCA_REAR
       #   -----------     \           /⁻\ 
       #                    \          ///
       #                     \ 
       #                      *LCA_FRONT
       #                     /⁻\ 
       #                     ///

    +-----------------+--------------------------+--------+
    | Points  Name    | Description              | Type   |
    +=================+==========================+========+
    | wheel center    | Center of the Wheel      | mobile |
    +-----------------+--------------------------+--------+
    | UCA FRONT       | Upper Control Arm Front  | fixed  |
    +-----------------+--------------------------+--------+
    | UCA REAR        | Upper Control Arm Rear   | fixed  |
    +-----------------+--------------------------+--------+
    | uca outer       | Upper Control Arm Outer  | mobile |
    +-----------------+--------------------------+--------+
    | LCA FRONT       | Lower Control Arm Front  | fixed  |
    +-----------------+--------------------------+--------+
    | LCA REAR        | Lower Control Arm Rear   | fixed  |
    +-----------------+--------------------------+--------+
    | lca outer       | Lower Control Arm Outer  | mobile |
    +-----------------+--------------------------+--------+
    | TIEROD INNER    | Inner Tie Rod            | fixed  |
    +-----------------+--------------------------+--------+
    | tierod outer    | Outer Tie Rod            | mobile |
    +-----------------+--------------------------+--------+

    """

    if path is None:
        path = os.getcwd()
 
    prepare_simulation(path, result_folder_name)
    logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)
 
    wheel, index = generate_wheel_center_heights(
        data["wheel_center"], max_height_increase, max_height_decrease, height_step)

    def get_L():
        L = np.array([
            data["uca_outer"] - data["UCA_FRONT"],
            data["uca_outer"] - data["UCA_REAR"],
            data["lca_outer"] - data["LCA_FRONT"],
            data["lca_outer"] - data["LCA_REAR"],
            data["tierod_outer"] - data["TIEROD_INNER"],
            data["tierod_outer"] - data["uca_outer"],
            data["tierod_outer"] - data["lca_outer"],
            data["lca_outer"] - data["uca_outer"],
            data["wheel_center"] - data["uca_outer"],
            data["wheel_center"] - data["lca_outer"],
            data["wheel_center"] - data["tierod_outer"],
        ])
        return L

    L_squared = np.linalg.norm(get_L(), axis=1)**2
    
    def jacobian(x, _):
        
        J = np.zeros([len(x), len(x)])

        # EQ0 (1)
        J[0, 0] = 2 * (x[0] - data["UCA_FRONT"][0])
        J[0, 1] = 2 * (x[1] - data["UCA_FRONT"][1])
        J[0, 2] = 2 * (x[2] - data["UCA_FRONT"][2])

        # EQ1 (1)
        J[1, 0] = 2 * (x[0] - data["UCA_REAR"][0])
        J[1, 1] = 2 * (x[1] - data["UCA_REAR"][1])
        J[1, 2] = 2 * (x[2] - data["UCA_REAR"][2])

        # EQ2 (2)
        J[2, 3] = 2 * (x[3] - data["LCA_FRONT"][0])
        J[2, 4] = 2 * (x[4] - data["LCA_FRONT"][1])
        J[2, 5] = 2 * (x[5] - data["LCA_FRONT"][2])

        # EQ3 (2)
        J[3, 3] = 2 * (x[3] - data["LCA_REAR"][0])
        J[3, 4] = 2 * (x[4] - data["LCA_REAR"][1])
        J[3, 5] = 2 * (x[5] - data["LCA_REAR"][2])

        # EQ4 (3)
        J[4, 6] = 2 * (x[6] - data["TIEROD_INNER"][0])
        J[4, 7] = 2 * (x[7] - data["TIEROD_INNER"][1])
        J[4, 8] = 2 * (x[8] - data["TIEROD_INNER"][2])

        # EQ5 (3 1)
        J[5, 0] = 2 * (x[0] - x[6])
        J[5, 1] = 2 * (x[1] - x[7])
        J[5, 2] = 2 * (x[2] - x[8])

        J[5, 6] = -2 * (x[0] - x[6])
        J[5, 7] = -2 * (x[1] - x[7])
        J[5, 8] = -2 * (x[2] - x[8])

        # EQ6 (3, 2)
        J[6, 3] = 2 * (x[3] - x[6])
        J[6, 4] = 2 * (x[4] - x[7])
        J[6, 5] = 2 * (x[5] - x[8])

        J[6, 6] = -2 * (x[3] - x[6])
        J[6, 7] = -2 * (x[4] - x[7])
        J[6, 8] = -2 * (x[5] - x[8])

        # EQ7 (2, 1)
        J[7, 0] = 2 * (x[0] - x[3])
        J[7, 1] = 2 * (x[1] - x[4])
        J[7, 2] = 2 * (x[2] - x[5])

        J[7, 3] = -2 * (x[0] - x[3])
        J[7, 4] = -2 * (x[1] - x[4])
        J[7, 5] = -2 * (x[2] - x[5])

        # EQ8 (4, 1)
        J[8, 0] = 2 * (x[0] - x[9])
        J[8, 1] = 2 * (x[1] - x[10])
        J[8, 2] = 2 * (x[2] - x[11])

        J[8, 9] = -2 * (x[0] - x[9])
        J[8, 10] = -2 * (x[1] - x[10])
        J[8, 11] = -2 * (x[2] - x[11])

        # EQ9 (4, 2)
        J[9, 3] = 2 * (x[3] - x[9])
        J[9, 4] = 2 * (x[4] - x[10])
        J[9, 5] = 2 * (x[5] - x[11])

        J[9, 9] = -2 * (x[3] - x[9])
        J[9, 10] = -2 * (x[4] - x[10])
        J[9, 11] = -2 * (x[5] - x[11])

        # EQ10 (4, 3)
        J[10, 6] = 2 * (x[6] - x[9])
        J[10, 7] = 2 * (x[7] - x[10])
        J[10, 8] = 2 * (x[8] - x[11])

        J[10, 9] = -2 * (x[6] - x[9])
        J[10, 10] = -2 * (x[7] - x[10])
        J[10, 11] = -2 * (x[8] - x[11])

        # EQ11
        J[11, 11] = -1
        return J
    
    def residual(vars, wheel_center_z):
        uca_outer, lca_outer, tierod_outer, wheel_center = vars[
            0:3], vars[3:6], vars[6:9], vars[9:12]
        diff = np.array([
            uca_outer - data["UCA_FRONT"],
            uca_outer - data["UCA_REAR"],
            lca_outer - data["LCA_FRONT"],
            lca_outer - data["LCA_REAR"],
            tierod_outer - data["TIEROD_INNER"],
            tierod_outer - uca_outer,
            tierod_outer - lca_outer,
            lca_outer - uca_outer,
            wheel_center - uca_outer,
            wheel_center - lca_outer,
            wheel_center - tierod_outer,
        ])
        F = np.linalg.norm(diff, axis=1)**2 - L_squared

        return np.append(F, np.array([-wheel_center[2] + wheel_center_z]))

    initial_guess = [data["uca_outer"],
                     data["lca_outer"],
                     data["tierod_outer"],
                     data["wheel_center"]]
    
    solution_save = solve(wheel, index, initial_guess, residual, jacobian=jacobian)

    solution = {
        "UCA_FRONT": data["UCA_FRONT"],  
        "UCA_REAR": data["UCA_REAR"],      
        "LCA_FRONT": data["LCA_FRONT"],    
        "LCA_REAR": data["LCA_REAR"],
        "TIEROD_INNER": data["TIEROD_INNER"],
        "uca_outer": solution_save[:, 0:3],
        "lca_outer": solution_save[:, 3:6],
        "tierod_outer": solution_save[:, 6:9],
        "wheel_center": solution_save[:, 9:12],
        "index_reference": index
    }
    
    wheel_variables = get_wheel(solution)
    
    if save_to_txt:
        saved_defined_geometry(data, os.path.join(result_folder_name, "input_geometry.suspgeo"))
        save_results_2_txt(wheel_variables, os.path.join(result_folder_name, "wheel_variables.suspvar"))
        
    return solution, wheel_variables


def double_whisbone_configuration_1(data, max_height_increase, max_height_decrease, height_step, save_to_txt=True, result_folder_name="results", path=None):
    """
    Computes and solves the geometric constraints for a double wishbone suspension system.

    The function generates different wheel center heights based on input constraints, then calculates
    the residuals for a non-linear optimization problem to find the correct configuration of the
    suspension system.

    Parameters
    ----------
    Data : dict
        A dictionary containing the initial measurements and reference points for the suspension system.
        Expected keys include:
            - 'wheel_center': The initial wheel center position.
            - 'uca_outer': The outer UCA (Upper Control Arm) position.
            - 'UCA_FRONT': The front reference point for the UCA.
            - 'UCA_REAR': The rear reference point for the UCA.
            - 'lca_outer': The outer LCA (Lower Control Arm) position.
            - 'LCA_FRONT': The front reference point for the LCA.
            - 'LCA_REAR': The rear reference point for the LCA.
            - 'tierod_outer': The outer tierod position.
            - 'TIEROD_INNER': The inner reference point for the tierod.
    max_height_increase : float
        Maximum increase in wheel center height for the analysis.
    max_height_decrease : float
        Maximum decrease in wheel center height for the analysis.
    height_step : float
        Step size for incrementing and decrementing the wheel center height.
    save_to_txt : bool, optional
        If True, the results will be saved to a text file. Default is True.

    Returns
    -------
    solution : dict
        A dictionary with the optimized suspension parameters and their values:
            - 'UCA_FRONT': The front UCA position.
            - 'UCA_REAR': The rear UCA position.
            - 'LCA_FRONT': The front LCA position.
            - 'LCA_REAR': The rear LCA position.
            - 'TIEROD_INNER': The inner tierod position.
            - 'uca_outer': Optimized outer UCA positions.
            - 'lca_outer': Optimized outer LCA positions.
            - 'tierod_outer': Optimized outer tierod positions.
            - 'wheel_center': Optimized wheel center positions.
            - 'index_reference': Index reference for the wheel center heights.

    Notes
    -----
    The function utilizes an optimization algorithm to solve for the configuration of the suspension
    system that satisfies the geometric constraints. The geometric model assumes a double wishbone
    suspension layout with specific reference points for each component.
   
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
       #    |       | uca_outer   /⁻\ 
       #    |       |             ///
       #    |       |                        * U_SPRING_MOUNT
       #    |  wheel center                 /
       #    |   *   |        tierod_outer  .
       #    |       |       *-------------/------*TIEROD_INNER
       #    |       |                    .
       #    |       |                   /
       #    |       |     lca_outer    .
       #    |       |     *-----------/-*LCA_REAR
       #    |       |      \         . /⁻\ 
       #   -----------      \       /  ///
       #                     \     .
       #                      \   * l_spring_mount 
       #                       \ 
       #                        *LCA_FRONT
       #                       /⁻\ 
       #                       ///

    +-----------------+--------------------------+--------+
    | Points  Name    | Description              | Type   |
    +=================+==========================+========+
    | wheel center    | Center of the Wheel      | mobile |
    +-----------------+--------------------------+--------+
    | UCA FRONT       | Upper Control Arm Front  | fixed  |
    +-----------------+--------------------------+--------+
    | UCA REAR        | Upper Control Arm Rear   | fixed  |
    +-----------------+--------------------------+--------+
    | uca outer       | Upper Control Arm Outer  | mobile |
    +-----------------+--------------------------+--------+
    | LCA FRONT       | Lower Control Arm Front  | fixed  |
    +-----------------+--------------------------+--------+
    | LCA REAR        | Lower Control Arm Rear   | fixed  |
    +-----------------+--------------------------+--------+
    | lca outer       | Lower Control Arm Outer  | mobile |
    +-----------------+--------------------------+--------+
    | TIEROD INNER    | Inner Tie Rod            | fixed  |
    +-----------------+--------------------------+--------+
    | tierod outer    | Outer Tie Rod            | mobile |
    +-----------------+--------------------------+--------+
    | Spring/Damper   | Supensión Superior       | mobile |
    | Upper Mount     |                          |        |
    +-----------------+--------------------------+--------+
    | Spring/Damper   | Supensión Inferior       | mobile |
    | Lower Mount     |                          |        |
    +-----------------+--------------------------+--------+


    """
    if path is None:
        path = os.getcwd()
        
    prepare_simulation(path, result_folder_name)
    logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)

    wheel, index = generate_wheel_center_heights(
        data["wheel_center"], max_height_increase, max_height_decrease, height_step)

    def get_L():
        L = np.array([
            data["uca_outer"] - data["UCA_FRONT"],
            data["uca_outer"] - data["UCA_REAR"],
            data["lca_outer"] - data["LCA_FRONT"],
            data["lca_outer"] - data["LCA_REAR"],
            data["tierod_outer"] - data["TIEROD_INNER"],
            data["tierod_outer"] - data["uca_outer"],
            data["tierod_outer"] - data["lca_outer"],
            data["lca_outer"] - data["uca_outer"],
            data["wheel_center"] - data["uca_outer"],
            data["wheel_center"] - data["lca_outer"],
            data["wheel_center"] - data["tierod_outer"],
            data["l_spring_mount"] - data["LCA_FRONT"],
            data["l_spring_mount"] - data["LCA_REAR"],
            data["l_spring_mount"] - data["lca_outer"],
        ])

        return L

    L_squared = np.linalg.norm(get_L(), axis=1)**2

    def residual(vars, wheel_center_z):
        uca_outer, lca_outer, tierod_outer, wheel_center, l_spring_mount = vars[
            0:3], vars[3:6], vars[6:9], vars[9:12], vars[12:15]
        diff = np.array([
            uca_outer - data["UCA_FRONT"],
            uca_outer - data["UCA_REAR"],
            lca_outer - data["LCA_FRONT"],
            lca_outer - data["LCA_REAR"],
            tierod_outer - data["TIEROD_INNER"],
            tierod_outer - uca_outer,
            tierod_outer - lca_outer,
            lca_outer - uca_outer,
            wheel_center - uca_outer,
            wheel_center - lca_outer,
            wheel_center - tierod_outer,
            l_spring_mount - data["LCA_FRONT"],
            l_spring_mount - data["LCA_REAR"],
            l_spring_mount - lca_outer,
        ])
        F = np.linalg.norm(diff, axis=1)**2 - L_squared
        return np.append(F, np.array([wheel_center[2] - wheel_center_z]))

    initial_guess = [data["uca_outer"],
                     data["lca_outer"],
                     data["tierod_outer"], 
                     data["wheel_center"], 
                     data["l_spring_mount"]]
    
    solution_save = solve(wheel, index, initial_guess, residual, jacobian=None)

    solution = {
        "UCA_FRONT": data["UCA_FRONT"],
        "UCA_REAR": data["UCA_REAR"],
        "LCA_FRONT": data["LCA_FRONT"],
        "LCA_REAR": data["LCA_REAR"],
        "TIEROD_INNER": data["TIEROD_INNER"],
        "U_SPRING_MOUNT": data["U_SPRING_MOUNT"],
        "uca_outer": solution_save[:, 0:3],
        "lca_outer": solution_save[:, 3:6],
        "tierod_outer": solution_save[:, 6:9],
        "wheel_center": solution_save[:, 9:12],
        "l_spring_mount": solution_save[:, 12:15],
        "index_reference": index
    }

    wheel_variables = get_wheel(solution)
    
    if save_to_txt:
        saved_defined_geometry(data, os.path.join(result_folder_name, "input_geometry.suspgeo"))
        save_results_2_txt(wheel_variables, os.path.join(result_folder_name, "wheel_variables.suspvar"))
        
    return solution, wheel_variables



def double_whisbone_configuration_2(data, max_height_increase, max_height_decrease, height_step, save_to_txt=True, result_folder_name="results", path=None):
    """
    Computes and solves the geometric constraints for a double wishbone suspension system.

    The function generates different wheel center heights based on input constraints, then calculates
    the residuals for a non-linear optimization problem to find the correct configuration of the
    suspension system.

    Parameters
    ----------
    data : dict
        A dictionary containing the initial measurements and reference points for the suspension system.
        Expected keys include:
            - 'wheel_center': The initial wheel center position.
            - 'uca_outer': The outer UCA (Upper Control Arm) position.
            - 'UCA_FRONT': The front reference point for the UCA.
            - 'UCA_REAR': The rear reference point for the UCA.
            - 'lca_outer': The outer LCA (Lower Control Arm) position.
            - 'LCA_FRONT': The front reference point for the LCA.
            - 'LCA_REAR': The rear reference point for the LCA.
            - 'tierod_outer': The outer tierod position.
            - 'TIEROD_INNER': The inner reference point for the tierod.
            - 'push_rod_outer': The outer push rod position.
            - 'push_rod_inner': The inner push rod position.
            - 'ROCKER_PIVOT': The rocker pivot position.
            - 'ROCKER_PIVOT_AXIS': The rocker pivot axis position.
            - 'l_spring_mount': The lower spring mount position.
            - 'U_SPRING_MOUNT': The upper spring mount position.
    max_height_increase : float
        Maximum increase in wheel center height for the analysis.
    max_height_decrease : float
        Maximum decrease in wheel center height for the analysis.
    height_step : float
        Step size for incrementing and decrementing the wheel center height.
    save_to_txt : bool, optional
        If True, the results will be saved to a text file. Default is True.
    result_folder_name : str, optional
        The name of the folder where results will be saved. Default is "results".
    path : str, optional
        The path where the results folder will be created. If None, the current working directory is used. Default is None.

    Returns
    -------
    solution : dict
        A dictionary with the optimized suspension parameters and their values:
            - 'UCA_FRONT': The front UCA position.
            - 'UCA_REAR': The rear UCA position.
            - 'LCA_FRONT': The front LCA position.
            - 'LCA_REAR': The rear LCA position.
            - 'TIEROD_INNER': The inner tierod position.
            - 'uca_outer': Optimized outer UCA positions.
            - 'lca_outer': Optimized outer LCA positions.
            - 'tierod_outer': Optimized outer tierod positions.
            - 'wheel_center': Optimized wheel center positions.
            - 'push_rod_outer': Optimized outer push rod positions.
            - 'push_rod_inner': Optimized inner push rod positions.
            - 'l_spring_mount': Optimized lower spring mount positions.
            - 'index_reference': Index reference for the wheel center heights.

    Notes
    -----
    The function utilizes an optimization algorithm to solve for the configuration of the suspension
    system that satisfies the geometric constraints. The geometric model assumes a double wishbone
    suspension layout with specific reference points for each component.
    
    .. code-block::

       #                                        l_spring_mount
       #                                        *-\/\/\/\/\/\/\/\/\/\/--* U_SPRING_MOUNT
       #                    \\\                /|                      /⁻\ 
       #                    \-/  pushrod inner* |  *ROCKER PIVOT AXIS  ///
       #             uca_rear*               / \| /
       #                    /               /   *ROCKER PIVOT
       #                   /               /   /⁻\ 
       #   -----------    /  pushrod outer*    ///
       #    |       |    /
       #    |       |   *----------*uca_front
       #    |       | uca_outer   /⁻\ 
       #    |       |             ///
       #    |       |
       #    |  wheel center 
       #    |   *   |        tierod_outer
       #    |       |       *--------------------*tierod_inner
       #    |       |
       #    |       |
       #    |       |   lca_outer
       #    |       |      *------------*lca_rear
       #   -----------     \           /⁻\ 
       #                    \          ///
       #                     \ 
       #                      *lca_front
       #                     /⁻\ 
       #                     ///
    
    +-----------------+--------------------------+--------+
    | Points  Name    | Description              | Type   |
    +=================+==========================+========+
    | wheel center    | Center of the Wheel      | mobile |
    +-----------------+--------------------------+--------+
    | UCA FRONT       | Upper Control Arm Front  | fixed  |
    +-----------------+--------------------------+--------+
    | UCA REAR        | Upper Control Arm Rear   | fixed  |
    +-----------------+--------------------------+--------+
    | uca outer       | Upper Control Arm Outer  | mobile |
    +-----------------+--------------------------+--------+
    | LCA FRONT       | Lower Control Arm Front  | fixed  |
    +-----------------+--------------------------+--------+
    | LCA REAR        | Lower Control Arm Rear   | fixed  |
    +-----------------+--------------------------+--------+
    | lca outer       | Lower Control Arm Outer  | mobile |
    +-----------------+--------------------------+--------+
    | TIEROD INNER    | Inner Tie Rod            | fixed  |
    +-----------------+--------------------------+--------+
    | tierod outer    | Outer Tie Rod            | mobile |
    +-----------------+--------------------------+--------+
    | pushrod outer   | Pushrod Exterior         | mobile |
    +-----------------+--------------------------+--------+
    | pushrod inner   | Pushrod Interior         | mobile |
    +-----------------+--------------------------+--------+
    | ROCKER PIVOT    | Rocker pivot             | fixed  |
    +-----------------+--------------------------+--------+
    | ROCKER PIVOT    | Rocker pivot axis        | fixed  |
    | AXIS            |                          |        |
    +-----------------+--------------------------+--------+
    | U SPRING MOUNT  | Spring/damper            | fixed  |
    |                 |  Upper Mount             |        |
    +-----------------+--------------------------+--------+
    | l spring mount  | Spring/Damper            | mobile |
    |                 | Lower Mount              |        |
    +-----------------+--------------------------+--------+
    
    """

    if path is None:
        path = os.getcwd()
        
    prepare_simulation(path, result_folder_name)
    logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)
    
    wheel, index = generate_wheel_center_heights(
        data["wheel_center"], max_height_increase, max_height_decrease, height_step)

    def get_L():
        L = np.array([
            data["uca_outer"] - data["UCA_FRONT"],
            data["uca_outer"] - data["UCA_REAR"],
            data["lca_outer"] - data["LCA_FRONT"],
            data["lca_outer"] - data["LCA_REAR"],
            data["tierod_outer"] - data["TIEROD_INNER"],
            data["tierod_outer"] - data["uca_outer"],
            data["tierod_outer"] - data["lca_outer"],
            data["lca_outer"] - data["uca_outer"],
            data["wheel_center"] - data["uca_outer"],
            data["wheel_center"] - data["lca_outer"],
            data["wheel_center"] - data["tierod_outer"],
            data["push_rod_outer"] - data["UCA_FRONT"],
            data["push_rod_outer"] - data["UCA_REAR"], 
            data["push_rod_outer"] - data["uca_outer"],       
            data["push_rod_inner"] - data["push_rod_outer"],  
            data["push_rod_inner"] - data["ROCKED_PIVOT"],     
            data["push_rod_inner"] - data["ROCKED_PIVOT_AXIS"], 
            data["l_spring_mount"] - data["UCA_FRONT"],        
            data["l_spring_mount"] - data["ROCKED_PIVOT"],     
            data["l_spring_mount"] - data["push_rod_inner"],
        ])

        return L

    L_squared = np.linalg.norm(get_L(), axis=1)**2

    def residual(vars, wheel_center_z):
        uca_outer = vars[0:3]
        lca_outer = vars[3:6]
        tierod_outer = vars[6:9]
        wheel_center = vars[9:12]
        push_rod_outer = vars[12:15]
        push_rod_inner = vars[15:18]
        l_spring_mount = vars[18:21]
        diff = np.array([
            uca_outer - data["UCA_FRONT"], 
            uca_outer - data["UCA_REAR"],  
            lca_outer - data["LCA_FRONT"],  
            lca_outer - data["LCA_REAR"],
            tierod_outer - data["TIEROD_INNER"],  
            tierod_outer - uca_outer,  
            tierod_outer - lca_outer, 
            lca_outer - uca_outer, 
            wheel_center - uca_outer,  
            wheel_center - lca_outer,  
            wheel_center - tierod_outer,  
            push_rod_outer - data["UCA_FRONT"],    
            push_rod_outer - data["UCA_REAR"],        
            push_rod_outer - uca_outer, 
            push_rod_inner - push_rod_outer,
            push_rod_inner - data["ROCKED_PIVOT"],
            push_rod_inner - data["ROCKED_PIVOT_AXIS"],
            l_spring_mount - data["UCA_FRONT"],   
            l_spring_mount - data["ROCKED_PIVOT"],   
            l_spring_mount - push_rod_inner,
        ])
        F = np.linalg.norm(diff, axis=1)**2 - L_squared

        return np.append(F, np.array([-wheel_center[2] + wheel_center_z]))

    initial_guess = [data["uca_outer"], data["lca_outer"],
                     data["tierod_outer"], data["wheel_center"],
                     data["push_rod_outer"] , data["push_rod_inner"],
                     data["l_spring_mount"]]
    solution_save = solve(wheel, index, initial_guess, residual, jacobian=None)

    solution = {
        "UCA_FRONT": data["UCA_FRONT"],      
        "UCA_REAR": data["UCA_REAR"],         
        "LCA_FRONT": data["LCA_FRONT"],       
        "LCA_REAR": data["LCA_REAR"],           
        "TIEROD_INNER": data["TIEROD_INNER"],   
        "ROCKED_PIVOT": data["ROCKED_PIVOT"],   
        "ROCKED_PIVOT_AXIS": data["ROCKED_PIVOT_AXIS"], 
        "U_SPRING_MOUNT": data["U_SPRING_MOUNT"],
        "uca_outer": solution_save[:, 0:3],   
        "lca_outer": solution_save[:, 3:6],    
        "tierod_outer": solution_save[:, 6:9],  
        "wheel_center": solution_save[:, 9:12], 
        "push_rod_outer": solution_save[:, 12:15],
        "push_rod_inner": solution_save[:, 15:18], 
        "l_spring_mount": solution_save[:, 18:21], 
        "index_reference": index
    }

    wheel_variables = get_wheel(solution)
    
    if save_to_txt:
        saved_defined_geometry(data, os.path.join(result_folder_name, "input_geometry.suspgeo"))
        save_results_2_txt(wheel_variables, os.path.join(result_folder_name, "wheel_variables.suspvar"))
        
    return solution, wheel_variables
