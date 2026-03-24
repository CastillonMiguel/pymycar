Theory
******

Welcome to the theory section. Originally, pymycar was developed as a tool for creating vehicle dynamics models. This section provides detailed information about all the models implemented in pymycar. While the software initially focused on car analysis, its capabilities have since been extended to include motorcycle analysis. The current implementation supports both types of vehicles, enabling comprehensive kinematics analysis for both cars and motorcycles.

1. **14-DOF Vehicle Dynamics** (:ref:`theory_full_model`):
   
2. **Vertical Dynamics** (:ref:`theory_vertical_models`): This section describes the general framework for performing vertical analysis of both car suspension systems and motorcycles. It includes the analysis of forces and moments acting on the vehicle, as well as the equations of motion governing its vertical dynamics.

3. **Lateral Dynamics** (:ref:`theory_lateral_models`):

4. **Kinematic Models** (:ref:`theory_kinematic`): This section outlines the general framework for conducting kinematic analysis of car suspension systems and motorcycles.

5. **Car Suspension Kinematics** (:ref:`theory_suspensions_kinematics`): Here, the kinematic analysis focuses on car suspension systems, examining the kinematics of the wheels and the suspension. It covers double wishbone and multilink systems, and includes the analysis of variables such as wheelbase, camber, toe, etc.
   
.. 6. **Motorcycle Kinematics** (:ref:`theory_motorcycle_kinematics`): This part focuses on the kinematic analysis of motorcycles, detailing the kinematics of the wheels and suspension system. It covers components like telescopic forks and single shock absorbers, and includes the analysis of variables such as wheelbase, camber, toe, etc.

.. toctree::
   :hidden:

   vertical_models/main
   lateral_models/main
   full_model/main
   kinematic/main
   car_kinematics/main
   .. motorcycle_kinematics/main
