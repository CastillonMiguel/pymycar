"""
Motorcycle Rear Assembly Kinematics Analysis
============================================

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
from pymycar.CarKinematic.functions import solve
from pymycar.MotorCycleKinematic.functions import generate_axis_range # save_data
from pymycar.CarKinematic.suspension_files import saved_defined_geometry # save_data
from pymycar.CarKinematic.functions import get_wheel

def rear_bike_base(data, 
                   max_height_increase, 
                   max_height_decrease, 
                   height_step, 
                   save_to_txt=True, 
                   result_folder_name="results",
                   path = None):
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
            - 'wheel_center_rear': The initial wheel center position.
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

       #
       #
       #
       #
       #                                                  \ 
       #                                                   . 
       #                                                    \ 
       #        /--------------                ___________----* SA_LEFT
       #       /                              /             /⁻\\ 
       #      /                 _____________/              ///\ 
       #     / sa_left_outer  /                                 \ 
       #    /     *----------/                   ___________-----* SA_RIGHT
       #    \      \                             /              /⁻\\ 
       #  wheel center*            _____________/               /// . 
       #     \       \            /                                  \ 
       #      \       *----------/  
       #       \   SA_right_outer
       #        \
       #         \
       #          \---*----------
       #             Wheel center ground reference
       #

    +-----------------+--------------------------+--------+
    | Points  Name    | Description              | Type   |
    +=================+==========================+========+
    | wheel center    | Center of the Wheel      | mobile |
    +-----------------+--------------------------+--------+
    | wheel center GR | Wheel Center Ground Ref  | fixed  |
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

    +-----------------+--------------------------+--------+
    | Points  Name    | Description              | Type   |
    +=================+==========================+========+
    | wheel center    | Center of the Wheel      | mobile |
    +-----------------+--------------------------+--------+
    | wheel center GR | Wheel Center Ground Ref  | fixed  |
    +-----------------+--------------------------+--------+
    | SA LEFT         | Swingarm Left            | fixed  |
    +-----------------+--------------------------+--------+
    | SA_RIGHT        | Swingarm Right           | fixed  |
    +-----------------+--------------------------+--------+
    | sa_left_outer   | Swingarm left Outer      | mobile |
    +-----------------+--------------------------+--------+
    | sa_right_outer  | Swingarm right Outer     | mobile |
    +-----------------+--------------------------+--------+

    """

    if path is None:
        path = os.getcwd()
 
    prepare_simulation(path, result_folder_name)
    logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)
 
    wheel, index = generate_axis_range(
        data["wheel_center_rear"], max_height_increase, max_height_decrease, height_step, axis=2)

    def get_L():
        L = np.array([
            data["sa_right_outer"] - data["SA_RIGHT"],
            data["sa_right_outer"] - data["SA_LEFT"],
            data["sa_left_outer"] - data["SA_LEFT"],
            data["sa_left_outer"] - data["SA_RIGHT"],
            data["sa_left_outer"] - data["sa_right_outer"],
            data["wheel_center_rear"] - data["SA_LEFT"],
            data["wheel_center_rear"] - data["SA_RIGHT"],
            data["wheel_center_rear"] - data["sa_right_outer"],
        ])
        return L

    L_squared = np.linalg.norm(get_L(), axis=1)**2
        
    def residual(vars, wheel_center_z):
        sa_right_outer, sa_left_outer, wheel_center_rear = vars[
            0:3], vars[3:6], vars[6:9]
        diff = np.array([
            sa_right_outer - data["SA_RIGHT"],
            sa_right_outer - data["SA_LEFT"],
            sa_left_outer - data["SA_LEFT"],
            sa_left_outer - data["SA_RIGHT"],
            sa_left_outer - sa_right_outer,
            wheel_center_rear - data["SA_LEFT"],
            wheel_center_rear - data["SA_RIGHT"],
            wheel_center_rear - sa_right_outer,
        ])
        # Use relative distance difference (improves conditioning for large coordinates)
        L = np.sqrt(L_squared)
        # avoid division by zero
        L_safe = np.where(L == 0, 1.0, L)
        F = (np.linalg.norm(diff, axis=1) - L) / L_safe

        z_res = (-wheel_center_rear[2] + wheel_center_z) / (np.mean(L_safe) if np.mean(L_safe) != 0 else 1.0)
        res = np.append(F, np.array([z_res]))

        # Diagnostics: ensure residual has expected shape and report norms for debugging
        if res.shape != (9,):
            print("DEBUG: residual shape", res.shape, "expected (9,)")
            print("DEBUG: len(F)=", F.shape[0], "L_squared len=", L_squared.shape[0])
            print("DEBUG: sa_right_outer shape", sa_right_outer.shape, "sa_left_outer shape", sa_left_outer.shape, "wheel_center shape", wheel_center_rear.shape)
            raise ValueError(f"Residual shape mismatch: {res.shape}")

        res_norm = np.linalg.norm(res)
        if res_norm > 1e6:
            print("DEBUG: residual norm large", res_norm)

        return res
    initial_guess = [data["sa_right_outer"],
                     data["sa_left_outer"],
                     data["wheel_center_rear"]]
    
    solution_save = solve(wheel, index, initial_guess, residual, jacobian=None)

    solution = {
        "SA_RIGHT": data["SA_RIGHT"],  
        "SA_LEFT": data["SA_LEFT"],      
        "sa_right_outer": solution_save[:, 0:3],
        "sa_left_outer": solution_save[:, 3:6],
        "wheel_center_rear": solution_save[:, 6:9],
        "index_reference": index
    }
    
    wheel_variables = 0
    # get_wheel(solution)
    
    # if save_to_txt:
    #     saved_defined_geometry(data, os.path.join(result_folder_name, "input_geometry.suspgeo"))
    #     save_results_2_txt(wheel_variables, os.path.join(result_folder_name, "wheel_variables.suspvar"))
        
    return solution, wheel_variables


def rear_bike_base_cantilever(data, 
                   max_height_increase, 
                   max_height_decrease, 
                   height_step, 
                   save_to_txt=True, 
                   result_folder_name="results",
                   path = None):
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

       #
       #
       #
       #
       #                                                  \ 
       #                                                   . 
       #                                                    \ 
       #        /--------------                ___________----* SA_LEFT
       #       /                              /             /⁻\\ 
       #      /                 _____________/              ///\ 
       #     / sa_left_outer  /                                 \ 
       #    /     *----------/                   ___________-----* SA_RIGHT
       #    \      \                             /              /⁻\\ 
       #  wheel center*            _____________/               /// . 
       #     \       \            /                                  \ 
       #      \       *----------/  
       #       \   SA_right_outer
       #        \
       #         \
       #          \---*----------
       #             Wheel center ground reference
       #

    +-----------------+--------------------------+--------+
    | Points  Name    | Description              | Type   |
    +=================+==========================+========+
    | wheel center    | Center of the Wheel      | mobile |
    +-----------------+--------------------------+--------+
    | wheel center GR | Wheel Center Ground Ref  | fixed  |
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

    +-----------------+--------------------------+--------+
    | Points  Name    | Description              | Type   |
    +=================+==========================+========+
    | wheel center    | Center of the Wheel      | mobile |
    +-----------------+--------------------------+--------+
    | wheel center GR | Wheel Center Ground Ref  | fixed  |
    +-----------------+--------------------------+--------+
    | SA LEFT         | Swingarm Left            | fixed  |
    +-----------------+--------------------------+--------+
    | SA_RIGHT        | Swingarm Right           | fixed  |
    +-----------------+--------------------------+--------+
    | sa_left_outer   | Swingarm left Outer      | mobile |
    +-----------------+--------------------------+--------+
    | sa_right_outer  | Swingarm right Outer     | mobile |
    +-----------------+--------------------------+--------+

    """

    if path is None:
        path = os.getcwd()
 
    prepare_simulation(path, result_folder_name)
    logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)
 
    wheel, index = generate_axis_range(
        data["wheel_center_rear"], max_height_increase, max_height_decrease, height_step, axis=2)

    def get_L():
        L = np.array([
            data["sa_right_outer"] - data["SA_RIGHT"],
            data["sa_right_outer"] - data["SA_LEFT"],
            data["sa_left_outer"] - data["SA_LEFT"],
            data["sa_left_outer"] - data["SA_RIGHT"],
            data["sa_left_outer"] - data["sa_right_outer"],
            data["l_spring_mount"] - data["SA_RIGHT"],
            data["l_spring_mount"] - data["SA_LEFT"],
            data["l_spring_mount"] - data["sa_right_outer"],
            data["wheel_center_rear"] - data["SA_LEFT"],
            data["wheel_center_rear"] - data["SA_RIGHT"],
            data["wheel_center_rear"] - data["sa_right_outer"],
        ])
        return L

    L_squared = np.linalg.norm(get_L(), axis=1)**2
        
    def residual(vars, wheel_center_z):
        sa_right_outer, sa_left_outer, l_spring_mount, wheel_center_rear = vars[
            0:3], vars[3:6], vars[6:9], vars[9:12]
        diff = np.array([
            sa_right_outer - data["SA_RIGHT"],
            sa_right_outer - data["SA_LEFT"],
            sa_left_outer - data["SA_LEFT"],
            sa_left_outer - data["SA_RIGHT"],
            sa_left_outer - sa_right_outer,
            l_spring_mount - data["SA_RIGHT"],
            l_spring_mount - data["SA_LEFT"],
            l_spring_mount - sa_right_outer,
            wheel_center_rear - data["SA_LEFT"],
            wheel_center_rear - data["SA_RIGHT"],
            wheel_center_rear - sa_right_outer,
        ])
        # Use relative distance difference (improves conditioning for large coordinates)
        L = np.sqrt(L_squared)
        # avoid division by zero
        L_safe = np.where(L == 0, 1.0, L)
        F = (np.linalg.norm(diff, axis=1) - L) / L_safe

        z_res = (-wheel_center_rear[2] + wheel_center_z) / (np.mean(L_safe) if np.mean(L_safe) != 0 else 1.0)
        res = np.append(F, np.array([z_res]))

        # Diagnostics: ensure residual has expected shape and report norms for debugging
        if res.shape != (12,):
            print("DEBUG: residual shape", res.shape, "expected (12,)")
            print("DEBUG: len(F)=", F.shape[0], "L_squared len=", L_squared.shape[0])
            print("DEBUG: sa_right_outer shape", sa_right_outer.shape, "sa_left_outer shape", sa_left_outer.shape, "wheel_center shape", wheel_center_rear.shape)
            raise ValueError(f"Residual shape mismatch: {res.shape}")

        res_norm = np.linalg.norm(res)
        if res_norm > 1e6:
            print("DEBUG: residual norm large", res_norm)

        return res
    initial_guess = [data["sa_right_outer"],
                     data["sa_left_outer"],
                     data["l_spring_mount"],
                     data["wheel_center_rear"]]
    
    solution_save = solve(wheel, index, initial_guess, residual, jacobian=None)

    solution = {
        "SA_RIGHT": data["SA_RIGHT"],  
        "SA_LEFT": data["SA_LEFT"],  
        'U_SPRING_MOUNT': data["U_SPRING_MOUNT"],    
        "sa_right_outer": solution_save[:, 0:3],
        "sa_left_outer": solution_save[:, 3:6],
        "l_spring_mount": solution_save[:, 6:9],
        "wheel_center_rear": solution_save[:, 9:12],
        "index_reference": index
    }
    
    wheel_variables = 0
    # get_wheel(solution)
    
    # if save_to_txt:
    #     saved_defined_geometry(data, os.path.join(result_folder_name, "input_geometry.suspgeo"))
    #     save_results_2_txt(wheel_variables, os.path.join(result_folder_name, "wheel_variables.suspvar"))
        
    return solution, wheel_variables


def rear_bike_base_cantilever(data, 
                   max_height_increase, 
                   max_height_decrease, 
                   height_step, 
                   save_to_txt=True, 
                   result_folder_name="results",
                   path = None):
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

       #
       #
       #
       #
       #                                                  \ 
       #                                                   . 
       #                                                    \ 
       #        /--------------                ___________----* SA_LEFT
       #       /                              /             /⁻\\ 
       #      /                 _____________/              ///\ 
       #     / sa_left_outer  /                                 \ 
       #    /     *----------/                   ___________-----* SA_RIGHT
       #    \      \                             /              /⁻\\ 
       #  wheel center*            _____________/               /// . 
       #     \       \            /                                  \ 
       #      \       *----------/  
       #       \   SA_right_outer
       #        \
       #         \
       #          \---*----------
       #             Wheel center ground reference
       #

    +-----------------+--------------------------+--------+
    | Points  Name    | Description              | Type   |
    +=================+==========================+========+
    | wheel center    | Center of the Wheel      | mobile |
    +-----------------+--------------------------+--------+
    | wheel center GR | Wheel Center Ground Ref  | fixed  |
    +-----------------+--------------------------+--------+
    | SA LEFT         | Swingarm Left            | fixed  |
    +-----------------+--------------------------+--------+
    | SA_RIGHT        | Swingarm Right           | fixed  |
    +-----------------+--------------------------+--------+
    | sa_left_outer   | Swingarm left Outer      | mobile |
    +-----------------+--------------------------+--------+
    | sa_right_outer  | Swingarm right Outer     | mobile |
    +-----------------+--------------------------+--------+

    """

    if path is None:
        path = os.getcwd()
 
    prepare_simulation(path, result_folder_name)
    logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)
 
    wheel, index = generate_axis_range(
        data["wheel_center_rear"], max_height_increase, max_height_decrease, height_step, axis=2)

    def get_L():
        L = np.array([
            data["sa_right_outer"] - data["SA_RIGHT"],
            data["sa_right_outer"] - data["SA_LEFT"],
            data["sa_left_outer"] - data["SA_LEFT"],
            data["sa_left_outer"] - data["SA_RIGHT"],
            data["sa_left_outer"] - data["sa_right_outer"],
            data["l_spring_mount"] - data["SA_RIGHT"],
            data["l_spring_mount"] - data["SA_LEFT"],
            data["l_spring_mount"] - data["sa_right_outer"],
            data["wheel_center_rear"] - data["SA_LEFT"],
            data["wheel_center_rear"] - data["SA_RIGHT"],
            data["wheel_center_rear"] - data["sa_right_outer"],
        ])
        return L

    L_squared = np.linalg.norm(get_L(), axis=1)**2
        
    def residual(vars, wheel_center_z):
        sa_right_outer, sa_left_outer, l_spring_mount, wheel_center_rear = vars[
            0:3], vars[3:6], vars[6:9], vars[9:12]
        diff = np.array([
            sa_right_outer - data["SA_RIGHT"],
            sa_right_outer - data["SA_LEFT"],
            sa_left_outer - data["SA_LEFT"],
            sa_left_outer - data["SA_RIGHT"],
            sa_left_outer - sa_right_outer,
            l_spring_mount - data["SA_RIGHT"],
            l_spring_mount - data["SA_LEFT"],
            l_spring_mount - sa_right_outer,
            wheel_center_rear - data["SA_LEFT"],
            wheel_center_rear - data["SA_RIGHT"],
            wheel_center_rear - sa_right_outer,
        ])
        # Use relative distance difference (improves conditioning for large coordinates)
        L = np.sqrt(L_squared)
        # avoid division by zero
        L_safe = np.where(L == 0, 1.0, L)
        F = (np.linalg.norm(diff, axis=1) - L) / L_safe

        z_res = (-wheel_center_rear[2] + wheel_center_z) / (np.mean(L_safe) if np.mean(L_safe) != 0 else 1.0)
        res = np.append(F, np.array([z_res]))

        # Diagnostics: ensure residual has expected shape and report norms for debugging
        if res.shape != (12,):
            print("DEBUG: residual shape", res.shape, "expected (12,)")
            print("DEBUG: len(F)=", F.shape[0], "L_squared len=", L_squared.shape[0])
            print("DEBUG: sa_right_outer shape", sa_right_outer.shape, "sa_left_outer shape", sa_left_outer.shape, "wheel_center shape", wheel_center_rear.shape)
            raise ValueError(f"Residual shape mismatch: {res.shape}")

        res_norm = np.linalg.norm(res)
        if res_norm > 1e6:
            print("DEBUG: residual norm large", res_norm)

        return res
    initial_guess = [data["sa_right_outer"],
                     data["sa_left_outer"],
                     data["l_spring_mount"],
                     data["wheel_center_rear"]]
    
    solution_save = solve(wheel, index, initial_guess, residual, jacobian=None)

    solution = {
        "SA_RIGHT": data["SA_RIGHT"],  
        "SA_LEFT": data["SA_LEFT"],  
        'U_SPRING_MOUNT': data["U_SPRING_MOUNT"],    
        "sa_right_outer": solution_save[:, 0:3],
        "sa_left_outer": solution_save[:, 3:6],
        "l_spring_mount": solution_save[:, 6:9],
        "wheel_center_rear": solution_save[:, 9:12],
        "index_reference": index
    }
    
    wheel_variables = 0
    # get_wheel(solution)
    
    # if save_to_txt:
    #     saved_defined_geometry(data, os.path.join(result_folder_name, "input_geometry.suspgeo"))
    #     save_results_2_txt(wheel_variables, os.path.join(result_folder_name, "wheel_variables.suspvar"))
        
    return solution, wheel_variables
