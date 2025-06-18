"""
.. _ref_vertical_models_full_car_example:

Vertical full car
^^^^^^^^^^^^^^^^^


"""

from pymycar.files import prepare_simulation, append_results_to_file
from pymycar.Logger.library_versions import set_logger, log_library_versions, log_system_info, log_end_analysis#, log_model_information

#Data.save_log_info(logger)  # log Simulation input data
 
from pymycar.Vehicle.car import MyCar
from pymycar.Vehicle.chassis import Chassis
from pymycar.Vehicle.suspension import Suspension, SimpleSuspension
from pymycar.Vehicle.wheel import Wheel

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


from pymycar.VerticalModels.models import VerticalQuarterCar
from pymycar.VerticalModels.exitations import sin_negative_part_exitation,sin_exitation

import os
path = os.getcwd()
result_folder_name = "solutions"
prepare_simulation(path, result_folder_name)
logger = set_logger(result_folder_name)
log_system_info(logger)  # log system imformation
log_library_versions(logger)  # log Library versions



chassis_class = Chassis(front_axle_to_com = 0.8, 
                  rear_axle_to_com = 0.8,
                  front_track=0.6,
                  rear_track=0.6,
                  com_height = 400,
                  mass=160,
                  inertia_x=100,
                  inertia_y=100,
                  inertia_z=1320,
                  drag_coefficient=0.34,
                  lift_coefficient=0.0) 

left_rear_wheel = Wheel(mass=10.0, 
                 spin_inertia=1.3, 
                 nominal_radius=100,
                 radial_stiffness=125560,
                 radial_damping=0.0,
                 nominal_vertical_load = 5000.0,
                 max_longitudinal_adherence=1.57,
                 max_lateral_adherence=1.41,
                 sidelsip_stiffness=25.0,
                 longitudinal_stiffness=34.0)

right_rear_wheel = Wheel(mass=10.0, 
                 spin_inertia=1.3, 
                 nominal_radius=100,
                 radial_stiffness=125560,
                 radial_damping=0.0,
                 nominal_vertical_load = 5000.0,
                 max_longitudinal_adherence=1.57,
                 max_lateral_adherence=1.41,
                 sidelsip_stiffness=25.0,
                 longitudinal_stiffness=34.0)

left_front_wheel = Wheel(mass=10.0, 
                 spin_inertia=1.3, 
                 nominal_radius=100,
                 radial_stiffness=125560,
                 radial_damping=0.0,
                 nominal_vertical_load = 5000.0,
                 max_longitudinal_adherence=1.57,
                 max_lateral_adherence=1.41,
                 sidelsip_stiffness=25.0,
                 longitudinal_stiffness=34.0)

right_front_wheel = Wheel(mass=10.0, 
                 spin_inertia=1.3, 
                 nominal_radius=100,
                 radial_stiffness=125560,
                 radial_damping=0.0,
                 nominal_vertical_load = 5000.0,
                 max_longitudinal_adherence=1.57,
                 max_lateral_adherence=1.41,
                 sidelsip_stiffness=25.0,
                 longitudinal_stiffness=34.0)


left_rear_suspension = SimpleSuspension(stiffness=35000,
                                          damper=2800)
right_rear_suspension = SimpleSuspension(stiffness=35000,
                                          damper=2800)
left_front_suspension = SimpleSuspension(stiffness=35000,
                                          damper=2800)
right_front_suspension = SimpleSuspension(stiffness=35000,
                                          damper=2800)

            
mycar = MyCar(chassis_class, 
              left_rear_wheel,
              right_rear_wheel,
              left_front_wheel, 
              right_front_wheel,
              left_rear_suspension,
              right_rear_suspension,
              left_front_suspension,
              right_front_suspension)

mycar.save_log_info(logger)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyvista as pv


from pymycar.VerticalModels.models import VerticalCar


def from_data(target_time):
    defined_time = np.linspace(0, 2, 1000)
    amplitude = 0.03
    frequency = 5.556/3
    sin_value = amplitude*np.sin(2 * np.pi * frequency * defined_time)
    aux = -np.maximum(sin_value, 0)
    defined_sol = np.interp(target_time, defined_time, aux)
    return 125560 * defined_sol #np.array([0.0, 125560 * defined_sol ])

def from_data2(target_time):
    defined_time = np.linspace(0, 2, 1000)
    amplitude = 0.03
    frequency = 5.556/3
    sin_value = amplitude*np.sin(2 * np.pi * frequency * defined_time)
    defined_sol = np.interp(target_time, defined_time, sin_value)
    return 125560 * defined_sol #np.array([0.0, 125560 * defined_sol ])

time_points = np.linspace(0, 2, 1000)

frequency = 5.556/3
amplitude = 0.03
sin_value=amplitude*np.sin(2 * np.pi * frequency * time_points)
aux = -np.maximum(sin_value, 0)
plt.plot(time_points, aux)
plt.show()

solver = VerticalCar(mycar, from_data2, time_points)
solution = solver.solve()
solver.plot_results()

plt.imshow(solver.K)
#plt.colorbar()
plt.show()


