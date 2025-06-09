"""
Suspension: Multilink
=====================

This module provides functions to analyze and simulate the behavior of a MUltilink suspension system.

"""

import os
import numpy as np

from pymycar.SuspensionKinematic.functions import solve, generate_wheel_center_heights
from pymycar.SuspensionKinematic.suspension_files import saved_defined_geometry # save_data
from pymycar.SuspensionKinematic.functions import get_wheel

from pymycar.files import prepare_simulation, save_results_2_txt
from pymycar.Logger.library_versions import logger_suspension_kinematics


def multilink(data, max_height_increase, max_height_decrease, height_step, save_to_txt=True, result_folder_name="results", path = None):
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
       #    |       |
       #    |       |
       #    |       |        tierod_outer
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

    +--------------+-------------------------------+
    | Name         | Description                   |
    +==============+===============================+
    | UCA_FRONT    | upper control arm front       |
    +--------------+-------------------------------+
    | UCA_REAR     | upper control arm rear        |
    +--------------+-------------------------------+
    | LCA_FRONT    | upper control arm front       |
    +--------------+-------------------------------+
    | LCA_REAR     | LOWER control arm rear        |
    +--------------+-------------------------------+
    | TIEROD_INNER | tierod inner                  |
    +--------------+-------------------------------+
    | uca_outer    | upper control arm outer       |
    +--------------+-------------------------------+
    | lca_outer    | lower upper control arm outer |
    +--------------+-------------------------------+
    | tierod_outer | tierod outer                  |
    +--------------+-------------------------------+

    Example
    -------
    >>> Data = {
    >>>     'wheel_center': np.array([0.0, 0.0, 0.0]),
    >>>     'uca_outer': np.array([1.0, 0.0, 0.0]),
    >>>     'UCA_FRONT': np.array([1.0, 1.0, 0.0]),
    >>>     'UCA_REAR': np.array([1.0, -1.0, 0.0]),
    >>>     'lca_outer': np.array([2.0, 0.0, 0.0]),
    >>>     'LCA_FRONT': np.array([2.0, 1.0, 0.0]),
    >>>     'LCA_REAR': np.array([2.0, -1.0, 0.0]),
    >>>     'tierod_outer': np.array([3.0, 0.0, 0.0]),
    >>>     'TIEROD_INNER': np.array([3.0, 0.5, 0.0])
    >>> }
    >>> max_height_increase = 0.2
    >>> max_height_decrease = 0.2
    >>> height_step = 0.05
    >>> result = double_whisbone(Data, max_height_increase, max_height_decrease, height_step)
    >>> print(result)
    """

    if path is None:
        path = os.getcwd()
  
    prepare_simulation(path, result_folder_name)
    logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)

    wheel, index = generate_wheel_center_heights(
        data["wheel_center"], max_height_increase, max_height_decrease, height_step)

    def get_L():
        L = np.array([
            data["uca_outer"] - data["UCA_FRONT"],         # 1
            data["uca_outer_aux"] - data["UCA_REAR"],      # 2
            data["lca_outer"] - data["LCA_FRONT"],         # 3
            data["lca_outer_aux"] - data["LCA_REAR"],      # 4
            data["tierod_outer"] - data["TIEROD_INNER"],   # 5
            data["lca_outer"] - data["uca_outer"],         # 6
            data["tierod_outer"] - data["uca_outer"],      # 7
            data["tierod_outer"] - data["lca_outer"],      # 8
            data["uca_outer_aux"] - data["uca_outer"],     # 9
            data["uca_outer_aux"] - data["lca_outer"],     # 10
            data["uca_outer_aux"] - data["tierod_outer"],  # 11
            data["lca_outer_aux"] - data["uca_outer"],     # 12
            data["lca_outer_aux"] - data["lca_outer"],     # 13
            data["lca_outer_aux"] - data["tierod_outer"],  # 14
            data["wheel_center"] - data["uca_outer"],      # 15
            data["wheel_center"] - data["lca_outer"],      # 16
            data["wheel_center"] - data["tierod_outer"],   # 17
        ])

        return L

    L_squared = np.linalg.norm(get_L(), axis=1)**2

    def residual(vars, wheel_center_z):
        uca_outer, lca_outer, tierod_outer, wheel_center = vars[0:3], vars[3:6], vars[6:9], vars[9:12]
        uca_outer_aux, lca_outer_aux = vars[12:15], vars[15:18]
        diff = np.array([
            uca_outer - data["UCA_FRONT"],         # 1
            uca_outer_aux - data["UCA_REAR"],      # 2
            lca_outer - data["LCA_FRONT"],         # 3
            lca_outer_aux - data["LCA_REAR"],      # 4
            tierod_outer - data["TIEROD_INNER"],   # 5
            lca_outer - uca_outer,                 # 6
            tierod_outer - uca_outer,              # 7
            tierod_outer - lca_outer,              # 8
            uca_outer_aux - uca_outer,             # 9
            uca_outer_aux - lca_outer,             # 10
            uca_outer_aux - tierod_outer,          # 11
            lca_outer_aux - uca_outer,             # 12
            lca_outer_aux - lca_outer,             # 13
            lca_outer_aux - tierod_outer,          # 14
            wheel_center - uca_outer,              # 15
            wheel_center - lca_outer,              # 16
            wheel_center - tierod_outer,           # 17
        ])
        F = np.linalg.norm(diff, axis=1)**2 - L_squared

        return np.append(F, np.array([-wheel_center[2] + wheel_center_z]))

    initial_guess = [
        data["uca_outer"],
        data["lca_outer"],
        data["tierod_outer"],
        data["wheel_center"],
        data["uca_outer_aux"],
        data["lca_outer_aux"]
    ]

    solution_save = solve(wheel, index, initial_guess, residual, jacobian=None)

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
        "uca_outer_aux": solution_save[:, 12:15],
        "lca_outer_aux": solution_save[:, 15:18],
        "index_reference": index
    }

    wheel_variables = get_wheel(solution)

    if save_to_txt:
        saved_defined_geometry(data, os.path.join(result_folder_name, "input_geometry.suspgeo"))
        save_results_2_txt(wheel_variables, os.path.join(result_folder_name, "wheel_variables.suspvar"))
        
    return solution, wheel_variables


def multilink_configuration_1(data, max_height_increase, max_height_decrease, height_step, save_to_txt=True, result_folder_name="results", path=None):
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
       #    |       |  uca_outer  /⁻\
       #    |       |             ///
       #    |       |
       #    |       |
       #    |       |        tierod_outer
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

    Example
    -------
    >>> Data = {
    >>>     'wheel_center': np.array([0.0, 0.0, 0.0]),
    >>>     'uca_outer': np.array([1.0, 0.0, 0.0]),
    >>>     'UCA_FRONT': np.array([1.0, 1.0, 0.0]),
    >>>     'UCA_REAR': np.array([1.0, -1.0, 0.0]),
    >>>     'lca_outer': np.array([2.0, 0.0, 0.0]),
    >>>     'LCA_FRONT': np.array([2.0, 1.0, 0.0]),
    >>>     'LCA_REAR': np.array([2.0, -1.0, 0.0]),
    >>>     'tierod_outer': np.array([3.0, 0.0, 0.0]),
    >>>     'TIEROD_INNER': np.array([3.0, 0.5, 0.0])
    >>> }
    >>> max_height_increase = 0.2
    >>> max_height_decrease = 0.2
    >>> height_step = 0.05
    >>> result = double_whisbone(Data, max_height_increase, max_height_decrease, height_step)
    >>> print(result)
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
