.. _theory_motorcycle_kinematics:

Motorcycle Kinematics
=====================

This section presents the kinematic analysis of motorcycles. When characterizing motorcycle kinematics, it is essential to clearly distinguish and properly define all the main structural components and the constraints acting between them.

In its most general form, a motorcycle can be divided into the following main parts:

.. table:: Main Motorcycle Parts

    +----------------+
    | Part           |
    +================+
    | Frame          |
    +----------------+
    | Rear assembly  |
    +----------------+
    | Front assembly |
    +----------------+

To perform a comprehensive kinematic analysis of the motorcycle, the approach is as follows. First, the analyses are performed on isolated subsystems:

* **Rear assembly kinematics:** This is analyzed considering the main frame as fixed. The most common configuration is the swingarm, although other designs exist. In a classical swingarm setup, the arm rotates around a fixed pivot point, which defines the kinematic trajectory of the rear wheel. The suspension spring and damper can be arranged in various ways, such as a cantilever design, a four-bar linkage, or other configurations that are also supported for analysis.

* **Front assembly kinematics:** This is also analyzed relative to a fixed frame. In the most general combination, the analysis involves both the steering motion and the wheel's vertical suspension travel, resulting in two degrees of freedom. The most common choice for this assembly is the telescopic fork, but alternative configurations can also be analyzed.

Separating the kinematic analysis into these subsystems facilitates the study of different component combinations. The complete spatial kinematics of the motorcycle are combined in a subsequent step to calculate and evaluate global parameters such as the wheelbase, steering geometry (e.g., rake and trail), and suspension ratios.

Additionally, the front and rear wheels are integrated into their respective assemblies. To properly define the overall kinematics, a detailed mathematical description of the wheel is introduced first.

.. toctree::
   :titlesonly:

   wheels/main
   rear_assembly/main
   front_assembly/main
