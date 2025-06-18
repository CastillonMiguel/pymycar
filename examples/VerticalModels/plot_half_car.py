"""
.. _ref_vertical_models_half_car_example:

Half car example
~~~~~~~~~~~~~~~~

Half car example
"""


from pymycar.files import prepare_simulation, append_results_to_file
from pymycar.Logger.library_versions import set_logger, log_library_versions, log_system_info, log_end_analysis#, log_model_information

 
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


left_front_suspension = SimpleSuspension(stiffness=35000,
                                          damper=2800)
right_front_suspension = SimpleSuspension(stiffness=35000,
                                          damper=2800)

            
mycar = MyCar(chassis=chassis_class,
              left_rear_wheel=None,
              right_rear_wheel=None,
              left_front_wheel=left_front_wheel, 
              right_front_wheel=right_front_wheel,
              left_rear_suspension=None,
              right_rear_suspension=None,
              left_front_suspension=left_front_suspension,
              right_front_suspension=right_front_suspension)



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyvista as pv

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyvista as pv


from pymycar.VerticalModels.models import VerticalHalfCar


def from_data(target_time):
    defined_time = np.linspace(0, 2, 100000)
    amplitude = 0.03
    frequency = 5.556/3
    sin_value = amplitude*np.sin(2 * np.pi * frequency * defined_time)
    aux = -np.maximum(sin_value, 0)
    defined_sol = np.interp(target_time, defined_time, aux)
    return 125560 * defined_sol #np.array([0.0, 125560 * defined_sol ])


time_points = np.linspace(0, 1, 10000)

frequency = 5.556/3
amplitude = 0.03
sin_value=amplitude*np.sin(2 * np.pi * frequency * time_points)
aux = -np.maximum(sin_value, 0)
plt.plot(time_points, aux)
plt.show()

solver = VerticalHalfCar(mycar, from_data, time_points)
solution = solver.solve()

Zs     = solution[:,0]
Ztheta = solution[:,1]
Zu1    = solution[:,2]
Zu2    = solution[:,3] 
Zs_dot = solution[:,4]
Ztheta_dot = solution[:,5]
Zu1_dot= solution[:,6]
Zu2_dot= solution[:,7]




fig, ax_q = plt.subplots() 
ax_q.plot(time_points, Zs,  'r-',   linewidth=2.0, label="Zs")
ax_q.plot(time_points, Zu1, 'g-',  linewidth=2.0, label="Zu1")
ax_q.plot(time_points, Zu2, 'b--', linewidth=2.0, label="Zu2")
ax_q.grid(color='k', linestyle='-', linewidth=0.3)
ax_q.set_xlabel('time' )  
ax_q.set_ylabel('displacement')    
ax_q.set_title('Displacement')   
ax_q.legend()

fig, ax_qa = plt.subplots() 
ax_qa.plot(time_points, Ztheta,  'y-',   linewidth=2.0, label="theta")
ax_qa.set_xlabel('time' )  
ax_qa.set_ylabel('angle')    
ax_qa.set_title('angle')   
ax_qa.legend()

fig, ax_q_dot = plt.subplots() 
ax_q_dot.plot(time_points, Zs_dot, 'r-', linewidth=2.0, label="Zs_dot")
ax_q_dot.plot(time_points, Zu1_dot, 'g-', linewidth=2.0, label="Zu1_dot")
ax_q_dot.plot(time_points, Zu2_dot, 'b--', linewidth=2.0, label="Zu2_dot")

#ax_q_dot.plot(time_points[:-1], np.diff(Zs)/np.diff(time_points), 'k--', linewidth=2.0, label="Zu_dot")
ax_q_dot.grid(color='k', linestyle='-', linewidth=0.3)
ax_q_dot.set_xlabel('time' )  
ax_q_dot.set_ylabel('velocity')    
ax_q_dot.set_title('Velocity')   
ax_q_dot.legend()
plt.show()
        