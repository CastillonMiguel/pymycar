r"""
.. _ref_plot_front_assembly_forks:

Front Assembly: Front Suspension Forks Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"""

###############################################################################
# Import necessary libraries
# --------------------------
from pymycar.MotorCycleKinematic.front_assembly import forks_system
import numpy as np

###############################################################################
# Parameters Definition
# ---------------------
data = {
    # --- Front assembly ---
    "wheel_center_front": np.array([650.0,   0.0,   -520.0]),
    "STEERING_AXIS_BOTTOM": np.array([650.0, 0.0,  -100.0]),
    "STEERING_AXIS_TOP":    np.array([570.0, 0.0,  250.0]),
    "fork_right_upper":  np.array([570.0, -110.0, 250.0]),
    "fork_left_upper":   np.array([570.0,  110.0, 250.0]),
    "fork_right_bottom": np.array([650.0, -120.0, -520.0]),
    "fork_left_bottom":  np.array([650.0,  120.0, -520.0]),
    # --- Rear assembly ---
    "wheel_center_rear": np.array([-600.0,   0.0,  -520.0]),  
    "SA_RIGHT": np.array([-100.0, -90.0, -300.0]),           
    "SA_LEFT":  np.array([-100.0,  90.0, -300.0]),
    "sa_right_outer": np.array([-600.0, -110.0, -520.0]), 
    "sa_left_outer":  np.array([-600.0,  110.0, -520.0]),
    "U_SPRING_MOUNT": np.array([-150.0, 0.0,  50.0]),
    "l_spring_mount": np.array([-420.0, 0.0, -350.0]),
}

import pyvista as pv

from pymycar.Cad.MotorCycle.front_assembly import fork_front_suspension_steer
from pymycar.Cad.MotorCycle.frame import frame_cad_base
from pymycar.Cad.MotorCycle.wheel import motorcycle_wheel

wheel = motorcycle_wheel(data["wheel_center_front"], data["fork_right_bottom"], data["fork_left_bottom"], ringradius=200, crosssectionradius=80)

steer_axis, top_part_steer, U_form = fork_front_suspension_steer(data)

plotter = pv.Plotter()
plotter.add_mesh(wheel, color="black", opacity=1.0)
plotter.add_mesh(steer_axis, color="blue")
plotter.add_mesh(top_part_steer, color="red")
plotter.add_mesh(U_form, color="green")


# Add points to the plot
for name, coord in data.items():
    plotter.add_mesh(pv.Sphere(radius=5, center=coord), color='red')

# Add text annotations
for name, coord in data.items():
    plotter.add_point_labels([coord], [name], point_size=20, font_size=30, text_color='black', always_visible=True)

plotter.show()


# file_path = 'data.suspgeo'
# data = load_defined_geometry("double_whisbone_base/input_geometry.suspgeo")

###############################################################################
# Call the Solver
# ---------------

drive_type = "mixed" # "steer", "bump" or "mixed"

solution, wheel_variables = forks_system(data,
                                max_height_increase=40,
                                max_height_decrease=40, 
                                height_step=1.0,
                                drive_type=drive_type,  # Passed dynamically 
                                max_steer_increase=40,
                                max_steer_decrease=40,
                                steer_step=5.0,
                                max_bump_increase=40,
                                max_bump_decrease=40,
                                bump_step=5.0,
                                save_to_txt=True,
                                result_folder_name="bike",
                                path = None)



from pymycar.Cad.geometric_forms import cylinder_from_two_points
from pymycar.Cad.MotorCycle.wheel import motorcycle_wheel


last_meshes = []
def plot_frame(plotter, data, index=None, bump_index=None, steer_index=None):
    global last_meshes

    if drive_type == "mixed":
        if bump_index is None or steer_index is None:
            bump_index, steer_index = data["index_reference"]
       
        wheel = motorcycle_wheel(data["wheel_center_front"][bump_index, steer_index], data["fork_right_bottom"][bump_index, steer_index], data["fork_left_bottom"][bump_index, steer_index], 200, 80)
        # wheel = cylinder_from_two_points(
        #     data["wheel_center"][bump_index, steer_index],
        #     data["fork_right_bottom"][bump_index, steer_index],
        #     data["fork_left_bottom"][bump_index, steer_index],
        #     height=50,
        #     radius=200,
        # )
        steer_axis, bar, U_form = fork_front_suspension_steer(solution, (bump_index, steer_index))
    else:
        if index is None:
            index = data["index_reference"]

        # swingarm, wheel_center1 = swingarm_cad_base(data, index)
        wheel = cylinder_from_two_points(data["wheel_center"][index], data["fork_right_bottom"][index], data["fork_left_bottom"][index], height=50, radius=200)

        steer_axis, bar, U_form = fork_front_suspension_steer(solution, index)
 
    # Remove the last meshes
    for mesh in last_meshes:
        plotter.remove_actor(mesh)

    # Add new meshes
    last_meshes = [
        plotter.add_mesh(steer_axis, color="blue"),
        plotter.add_mesh(bar, color="red"),
        plotter.add_mesh(U_form, color="blue"),
        plotter.add_mesh(wheel, color="black")
    ]


plotter = pv.Plotter()
def create_mesh_steer(value):
    if drive_type == "mixed":
        state["steer"] = np.abs(solution["steer_values"] - value).argmin()
        plot_frame(plotter, solution, bump_index=state["bump"], steer_index=state["steer"])
    else:
        res = np.abs(solution["fork_right_upper"][:,0] - value).argmin()
        plot_frame(plotter, solution, index=res)

def create_mesh_bump(value):
    if drive_type == "mixed":
        state["bump"] = np.abs(solution["bump_values"] - value).argmin()
        plot_frame(plotter, solution, bump_index=state["bump"], steer_index=state["steer"])
    else:
        res = np.abs(solution["wheel_center"][:,2] - value).argmin()
        plot_frame(plotter, solution, index=res)

state = {"bump": 0, "steer": 0}

if drive_type == "steer":
    plotter.add_slider_widget(create_mesh_steer,
                            rng=[solution["fork_right_upper"][0, 0], solution["fork_right_upper"][-1, 0]],
                            value=solution["fork_right_upper"][solution["index_reference"]][0],
                            title='Steer / Jounce (fork_right_upper x)')
else:
    if drive_type == "bump":
        plotter.add_slider_widget(create_mesh_bump,
                                rng=[solution["wheel_center"][0, 2], solution["wheel_center"][-1, 2]],
                                value=solution["wheel_center"][solution["index_reference"]][2],
                                title='Bump (wheel_center z)')
    else:
        state["bump"], state["steer"] = solution["index_reference"]
        plot_frame(plotter, solution, bump_index=state["bump"], steer_index=state["steer"])

        plotter.add_slider_widget(
            create_mesh_steer,
            rng=[solution["steer_values"][0], solution["steer_values"][-1]],
            value=solution["steer_values"][state["steer"]],
            title='Steer (fork_right_upper x)'
        )

        plotter.add_slider_widget(
            create_mesh_bump,
            rng=[solution["bump_values"][0], solution["bump_values"][-1]],
            value=solution["bump_values"][state["bump"]],
            title='Bump (wheel_center z)',
            pointa=(0.025, 0.15),
            pointb=(0.31, 0.15)
        )

plotter.show()
