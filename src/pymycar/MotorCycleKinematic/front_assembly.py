"""
Motorcycle Front Assembly Kinematics Analysis
=============================================

This module provides functions to analyze and simulate the behavior of a double wishbone suspension system. The double wishbone suspension is a type of vehicle suspension design that uses two wishbone-shaped arms (or control arms) to locate the wheel. This type of suspension is widely used in various vehicles, from road cars to competition vehicles.

"""


###############################################################################
# Import from pymycar package
# ---------------------------
import numpy as np

from pymycar.files import prepare_simulation, save_results_2_txt
from pymycar.Logger.library_versions import logger_suspension_kinematics
from pymycar.CarKinematic.functions import solve #, generate_wheel_center_heights
from pymycar.CarKinematic.suspension_files import saved_defined_geometry # save_data
from pymycar.CarKinematic.functions import get_wheel

import os
import numpy as np
from scipy.optimize import fsolve
from pymycar.MotorCycleKinematic.functions import generate_axis_range 


def forks_system(data, 
                   max_height_increase, 
                   max_height_decrease, 
                   height_step, 
                   drive_type="steer",
                   max_steer_increase=None,
                   max_steer_decrease=None,
                   steer_step=None,
                   max_bump_increase=None,
                   max_bump_decrease=None,
                   bump_step=None,
                   save_to_txt=True, 
                   result_folder_name="results",
                   path=None):
    """
    Solves the kinematics of a motorcycle front suspension system.
    """

    if path is None:
        path = os.getcwd()

    prepare_simulation(path, result_folder_name)
    logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)

    if drive_type == "steer":
        wheel, index = generate_axis_range(
            data["fork_right_upper"], max_height_increase, max_height_decrease, height_step, axis=0)
    elif drive_type == "bump":
        wheel, index = generate_axis_range(
            data["wheel_center_front"], max_height_increase, max_height_decrease, height_step, axis=2)
    elif drive_type == "mixed":
        if max_steer_increase is None:
            max_steer_increase = max_height_increase
        if max_steer_decrease is None:
            max_steer_decrease = max_height_decrease
        if steer_step is None:
            steer_step = height_step
        if max_bump_increase is None:
            max_bump_increase = max_height_increase
        if max_bump_decrease is None:
            max_bump_decrease = max_height_decrease
        if bump_step is None:
            bump_step = height_step

        steer_values, steer_index = generate_axis_range(
            data["fork_right_upper"], max_steer_increase, max_steer_decrease, steer_step, axis=0)
        bump_values, bump_index = generate_axis_range(
            data["wheel_center_front"], max_bump_increase, max_bump_decrease, bump_step, axis=2)
    else:
        raise ValueError("Invalid drive_type. Use 'steer', 'bump' or 'mixed'.")
     
    data["fork_right_middle"] = (data["fork_right_upper"] + data["fork_right_bottom"]) / 2
    data["fork_left_middle"] = (data["fork_left_upper"] + data["fork_left_bottom"]) / 2

    data["fork_right_middle_b"] = (data["fork_right_upper"] + data["fork_right_bottom"]) / 2
    data["fork_left_middle_b"] = (data["fork_left_upper"] + data["fork_left_bottom"]) / 2

    def get_L():
        L = np.array([
            data["fork_right_upper"] - data["STEERING_AXIS_TOP"],
            data["fork_right_upper"] - data["STEERING_AXIS_BOTTOM"],
            data["fork_left_upper"] - data["STEERING_AXIS_TOP"],
            data["fork_left_upper"] - data["STEERING_AXIS_BOTTOM"],
            data["fork_left_upper"] - data["fork_right_upper"], 
            data["fork_right_middle"] - data["STEERING_AXIS_TOP"],
            data["fork_right_middle"] - data["STEERING_AXIS_BOTTOM"],
            data["fork_right_middle"] - data["fork_right_upper"],
            data["fork_left_middle"] - data["STEERING_AXIS_TOP"],
            data["fork_left_middle"] - data["STEERING_AXIS_BOTTOM"],
            data["fork_left_middle"] - data["fork_left_upper"],
            data["fork_right_bottom"] - data["fork_left_bottom"],
            data["fork_right_middle_b"] - data["fork_right_bottom"],
            data["fork_left_middle_b"] - data["fork_left_bottom"],
            data["fork_right_bottom"] - data["fork_right_middle"],     # Add required base bottom distances to force DOF closing
            data["fork_left_bottom"] - data["fork_left_middle"],
            data["wheel_center_front"] - data["fork_right_bottom"],
            data["wheel_center_front"] - data["fork_left_bottom"],
            data["wheel_center_front"] - data["fork_right_middle_b"],
        ])
        return L

    L_squared = np.linalg.norm(get_L(), axis=1)**2
        
    def residual(vars, target_value):
        fork_right_upper, fork_left_upper, fork_right_middle, fork_left_middle, fork_right_bottom, fork_left_bottom, fork_right_middle_b, fork_left_middle_b, wheel_center_front = vars[0:3], vars[3:6], vars[6:9], vars[9:12], vars[12:15], vars[15:18], vars[18:21], vars[21:24], vars[24:27]
        diff = np.array([
            fork_right_upper - data["STEERING_AXIS_TOP"],
            fork_right_upper - data["STEERING_AXIS_BOTTOM"],
            fork_left_upper - data["STEERING_AXIS_TOP"],
            fork_left_upper - data["STEERING_AXIS_BOTTOM"],
            fork_left_upper - fork_right_upper, 
            fork_right_middle - data["STEERING_AXIS_TOP"],
            fork_right_middle - data["STEERING_AXIS_BOTTOM"],
            fork_right_middle - fork_right_upper,
            fork_left_middle - data["STEERING_AXIS_TOP"],
            fork_left_middle - data["STEERING_AXIS_BOTTOM"],
            fork_left_middle - fork_left_upper,
            fork_right_bottom - fork_left_bottom,
            fork_right_middle_b - fork_right_bottom,
            fork_left_middle_b - fork_left_bottom,
            fork_right_bottom - fork_right_middle,
            fork_left_bottom - fork_left_middle,
            wheel_center_front - fork_right_bottom,
            wheel_center_front - fork_left_bottom,
            wheel_center_front - fork_right_middle_b,
        ])
        
        L = np.sqrt(L_squared)
        L_safe = np.where(L == 0, 1.0, L)
        F = (np.linalg.norm(diff, axis=1) - L) / L_safe

        scale = np.mean(L_safe) if np.mean(L_safe) != 0 else 1.0
        if drive_type == "steer":
            target_res = (-fork_right_upper[0] + target_value) / scale
        elif drive_type == "bump":
            target_res = (-wheel_center_front[2] + target_value) / scale
        else:
            raise ValueError("Invalid drive_type. Use 'steer', 'bump' or 'mixed'.")
        
        v_upper_middle_R = diff[7] # fork_right_middle - fork_right_upper
        v_middle_bottom_R = diff[14] # fork_right_bottom - fork_right_middle
        
        # Normalize collinearity by typical lengths to keep residuals O(1)
        norm_R = (L_safe[14] * L_safe[7])
        collinear_Rx = (v_middle_bottom_R[0] * v_upper_middle_R[2] - v_middle_bottom_R[2] * v_upper_middle_R[0]) / norm_R
        collinear_Ry = (v_middle_bottom_R[1] * v_upper_middle_R[2] - v_middle_bottom_R[2] * v_upper_middle_R[1]) / norm_R
        
        v_upper_middle_L = diff[10] # fork_left_middle - fork_left_upper
        v_middle_bottom_L = diff[15] # fork_left_bottom - fork_left_middle
        
        norm_L = (L_safe[15] * L_safe[10])
        collinear_Lx = (v_middle_bottom_L[0] * v_upper_middle_L[2] - v_middle_bottom_L[2] * v_upper_middle_L[0]) / norm_L
        collinear_Ly = (v_middle_bottom_L[1] * v_upper_middle_L[2] - v_middle_bottom_L[2] * v_upper_middle_L[1]) / norm_L

        v_bottom_middle_Rb = diff[12] # fork_right_middle_b - fork_right_bottom
        norm_Rb = (L_safe[12] * L_safe[7])
        collinear_Rbx = (v_bottom_middle_Rb[0] * v_upper_middle_R[2] - v_bottom_middle_Rb[2] * v_upper_middle_R[0]) / norm_Rb
        collinear_Rby = (v_bottom_middle_Rb[1] * v_upper_middle_R[2] - v_bottom_middle_Rb[2] * v_upper_middle_R[1]) / norm_Rb

        v_bottom_middle_Lb = diff[13] # fork_left_middle_b - fork_left_bottom
        norm_Lb = (L_safe[13] * L_safe[10])
        collinear_Lbx = (v_bottom_middle_Lb[0] * v_upper_middle_L[2] - v_bottom_middle_Lb[2] * v_upper_middle_L[0]) / norm_Lb
        collinear_Lby = (v_bottom_middle_Lb[1] * v_upper_middle_L[2] - v_bottom_middle_Lb[2] * v_upper_middle_L[1]) / norm_Lb
        ext_arr = np.array([
            collinear_Rx, collinear_Ry,
            collinear_Lx, collinear_Ly,
            collinear_Rbx, collinear_Rby,
            collinear_Lbx, collinear_Lby
        ])

        if drive_type == "steer":
            # Keep steer behavior: all full-geometry lengths except one redundant bridge length.
            F_filtered = np.delete(F, 11)
            extra_arr = np.array([target_res])

        elif drive_type == "bump":
            # Keep bump behavior with full variable set:
            # - preserve only the same 6 bump lengths used in the original residual_bump
            # - pin upper and middle fork points so non-imposed steer geometry stays fixed
            bump_len_idx = [11, 12, 13, 16, 17, 18]
            F_filtered = F[bump_len_idx]

            pin_arr = np.array([
                (fork_right_upper[0] - data["fork_right_upper"][0]) / scale,
                (fork_right_upper[1] - data["fork_right_upper"][1]) / scale,
                (fork_right_upper[2] - data["fork_right_upper"][2]) / scale,
                (fork_left_upper[0] - data["fork_left_upper"][0]) / scale,
                (fork_left_upper[1] - data["fork_left_upper"][1]) / scale,
                (fork_left_upper[2] - data["fork_left_upper"][2]) / scale,
                (fork_right_middle[0] - data["fork_right_middle"][0]) / scale,
                (fork_right_middle[1] - data["fork_right_middle"][1]) / scale,
                (fork_right_middle[2] - data["fork_right_middle"][2]) / scale,
                (fork_left_middle[0] - data["fork_left_middle"][0]) / scale,
                (fork_left_middle[1] - data["fork_left_middle"][1]) / scale,
                (fork_left_middle[2] - data["fork_left_middle"][2]) / scale,
            ])

            extra_arr = np.concatenate((np.array([target_res]), pin_arr))

        elif drive_type == "mixed":
            raise ValueError("Use residual_mixed for drive_type='mixed'.")

        res = np.concatenate((F_filtered, ext_arr, extra_arr))

        if res.shape != (27,):
            raise ValueError(
                f"Residual shape mismatch: {res.shape} "
                f"(F_filtered={F_filtered.shape[0]}, ext_arr={ext_arr.shape[0]}, extra_arr={extra_arr.shape[0]})"
            )

        return res

    initial_guess = [data["fork_right_upper"],
                     data["fork_left_upper"],
                     data["fork_right_middle"],
                     data["fork_left_middle"],
                     data["fork_right_bottom"],
                     data["fork_left_bottom"],
                     data["fork_right_middle_b"],
                     data["fork_left_middle_b"],
                     data["wheel_center_front"]]

    if drive_type in ["steer", "bump"]:
        solution_save = solve(wheel, index, initial_guess, residual, jacobian=None)

        solution = {
            "STEERING_AXIS_TOP": data["STEERING_AXIS_TOP"],    
            "STEERING_AXIS_BOTTOM": data["STEERING_AXIS_BOTTOM"],
            "fork_right_upper": solution_save[:, 0:3],
            "fork_left_upper": solution_save[:, 3:6],
            "fork_right_middle": solution_save[:, 6:9],
            "fork_left_middle": solution_save[:, 9:12],
            "fork_right_bottom": solution_save[:, 12:15],
            "fork_left_bottom": solution_save[:, 15:18],
            "fork_right_middle_b": solution_save[:, 18:21],
            "fork_left_middle_b": solution_save[:, 21:24],
            "wheel_center_front": solution_save[:, 24:27],
            "index_reference": index
        }
    else:
        def residual_mixed(vars, steer_target, bump_target):
            fork_right_upper, fork_left_upper, fork_right_middle, fork_left_middle, fork_right_bottom, fork_left_bottom, fork_right_middle_b, fork_left_middle_b, wheel_center_front = vars[0:3], vars[3:6], vars[6:9], vars[9:12], vars[12:15], vars[15:18], vars[18:21], vars[21:24], vars[24:27]
            diff = np.array([
                fork_right_upper - data["STEERING_AXIS_TOP"],
                fork_right_upper - data["STEERING_AXIS_BOTTOM"],
                fork_left_upper - data["STEERING_AXIS_TOP"],
                fork_left_upper - data["STEERING_AXIS_BOTTOM"],
                fork_left_upper - fork_right_upper,
                fork_right_middle - data["STEERING_AXIS_TOP"],
                fork_right_middle - data["STEERING_AXIS_BOTTOM"],
                fork_right_middle - fork_right_upper,
                fork_left_middle - data["STEERING_AXIS_TOP"],
                fork_left_middle - data["STEERING_AXIS_BOTTOM"],
                fork_left_middle - fork_left_upper,
                fork_right_bottom - fork_left_bottom,
                fork_right_middle_b - fork_right_bottom,
                fork_left_middle_b - fork_left_bottom,
                fork_right_bottom - fork_right_middle,
                fork_left_bottom - fork_left_middle,
                wheel_center_front - fork_right_bottom,
                wheel_center_front - fork_left_bottom,
                wheel_center_front - fork_right_middle_b,
            ])

            L = np.sqrt(L_squared)
            L_safe = np.where(L == 0, 1.0, L)
            F = (np.linalg.norm(diff, axis=1) - L) / L_safe
            scale = np.mean(L_safe) if np.mean(L_safe) != 0 else 1.0

            v_upper_middle_R = diff[7]
            v_middle_bottom_R = diff[14]
            norm_R = (L_safe[14] * L_safe[7])
            collinear_Rx = (v_middle_bottom_R[0] * v_upper_middle_R[2] - v_middle_bottom_R[2] * v_upper_middle_R[0]) / norm_R
            collinear_Ry = (v_middle_bottom_R[1] * v_upper_middle_R[2] - v_middle_bottom_R[2] * v_upper_middle_R[1]) / norm_R

            v_upper_middle_L = diff[10]
            v_middle_bottom_L = diff[15]
            norm_L = (L_safe[15] * L_safe[10])
            collinear_Lx = (v_middle_bottom_L[0] * v_upper_middle_L[2] - v_middle_bottom_L[2] * v_upper_middle_L[0]) / norm_L
            collinear_Ly = (v_middle_bottom_L[1] * v_upper_middle_L[2] - v_middle_bottom_L[2] * v_upper_middle_L[1]) / norm_L

            v_bottom_middle_Rb = diff[12]
            norm_Rb = (L_safe[12] * L_safe[7])
            collinear_Rbx = (v_bottom_middle_Rb[0] * v_upper_middle_R[2] - v_bottom_middle_Rb[2] * v_upper_middle_R[0]) / norm_Rb
            collinear_Rby = (v_bottom_middle_Rb[1] * v_upper_middle_R[2] - v_bottom_middle_Rb[2] * v_upper_middle_R[1]) / norm_Rb

            v_bottom_middle_Lb = diff[13]
            norm_Lb = (L_safe[13] * L_safe[10])
            collinear_Lbx = (v_bottom_middle_Lb[0] * v_upper_middle_L[2] - v_bottom_middle_Lb[2] * v_upper_middle_L[0]) / norm_Lb
            collinear_Lby = (v_bottom_middle_Lb[1] * v_upper_middle_L[2] - v_bottom_middle_Lb[2] * v_upper_middle_L[1]) / norm_Lb

            ext_arr = np.array([
                collinear_Rx, collinear_Ry,
                collinear_Lx, collinear_Ly,
                collinear_Rbx, collinear_Rby,
                collinear_Lbx, collinear_Lby
            ])

            # Mixed mode: allow telescopic travel (drop 14,15), impose both steer and bump targets.
            F_filtered = np.delete(F, [14, 15])
            target_arr = np.array([
                (-fork_right_upper[0] + steer_target) / scale,
                (-wheel_center_front[2] + bump_target) / scale
            ])

            res = np.concatenate((F_filtered, ext_arr, target_arr))
            if res.shape != (27,):
                raise ValueError(
                    f"Residual shape mismatch (mixed): {res.shape} "
                    f"(F_filtered={F_filtered.shape[0]}, ext_arr={ext_arr.shape[0]}, target_arr={target_arr.shape[0]})"
                )
            return res

        n_bump = len(bump_values)
        n_steer = len(steer_values)
        solution_grid = np.zeros((n_bump, n_steer, 27))
        guess0 = np.concatenate(initial_guess)

        for ib, bump_target in enumerate(bump_values):
            for isr, steer_target in enumerate(steer_values):
                if ib == 0 and isr == 0:
                    guess = guess0
                elif isr > 0:
                    guess = solution_grid[ib, isr - 1, :]
                else:
                    guess = solution_grid[ib - 1, 0, :]

                sol = fsolve(
                    residual_mixed,
                    guess,
                    args=(steer_target, bump_target),
                    xtol=1e-10,
                    maxfev=0,
                )
                solution_grid[ib, isr, :] = sol

        solution = {
            "STEERING_AXIS_TOP": data["STEERING_AXIS_TOP"],
            "STEERING_AXIS_BOTTOM": data["STEERING_AXIS_BOTTOM"],
            "fork_right_upper": solution_grid[:, :, 0:3],
            "fork_left_upper": solution_grid[:, :, 3:6],
            "fork_right_middle": solution_grid[:, :, 6:9],
            "fork_left_middle": solution_grid[:, :, 9:12],
            "fork_right_bottom": solution_grid[:, :, 12:15],
            "fork_left_bottom": solution_grid[:, :, 15:18],
            "fork_right_middle_b": solution_grid[:, :, 18:21],
            "fork_left_middle_b": solution_grid[:, :, 21:24],
            "wheel_center_front": solution_grid[:, :, 24:27],
            "steer_values": steer_values,
            "bump_values": bump_values,
            "index_reference": (bump_index, steer_index)
        }
    
    wheel_variables = 0
    # get_wheel(solution)
    
    # if save_to_txt:
    #     saved_defined_geometry(data, os.path.join(result_folder_name, "input_geometry.suspgeo"))
    #     save_results_2_txt(wheel_variables, os.path.join(result_folder_name, "wheel_variables.suspvar"))
        
    return solution, wheel_variables
