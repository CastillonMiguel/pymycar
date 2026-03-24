.. _theory_suspensions_kinematics:

Suspension Analysis
-------------------

The **pyMyCar** model incorporates detailed suspension behavior through the use of lookup table information. This allows the model to relate the wheel jounce (relative displacement of the wheel with respect to the car chassis) to various dynamic variables, tire models, and other factors influencing vehicle dynamics.

Understanding the suspension system is crucial for accurately modeling the vehicle's behavior. Key variables such as the orientation of the wheel (including camber angle, toe angle, and side-view angle) and suspension characteristics (such as reduced stiffness) play a significant role in the overall dynamics of the vehicle.

The primary goal of this module is to determine these variables and save them as lookup table data for use in complete vehicle simulations.

The process for obtaining these variables involves defining constraint equations that uniquely describe the suspension system. By imposing variations, such as vertical displacement of the wheel, we can obtain the new values of the variables of interest.

The steps involved in the suspension analysis are as follows:

1. Define constraint equations that uniquely describe the suspension system.
2. Impose variations on the system, such as vertical displacement of the wheel or steering input.
3. Perform kinematic analysis to derive variables of interest and calculate the descriptive coordinates of all the suspension elements.
4. Knowing the coordinates, it will be possible to obtain variables such as wheelbase, track width, wheel orientation, and reduced stiffness.
5. Save these variables as lookup table data.

By completing the kinematic analysis, we can gain valuable insights into the suspension system's behavior and its impact on the vehicle's dynamics.

In the next sections, we will delve into the general approach followed to perform kinematic analysis, how to apply it to different suspension configurations (including double-wishbone, multi-link, and other setups), and finally, how some interesting variables are obtained from the coordinates derived in the kinematic analysis.


.. toctree::
   :titlesonly:

   double_whisbone/main
   multilink/main
   parameters/main