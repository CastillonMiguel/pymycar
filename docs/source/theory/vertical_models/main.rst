.. _theory_vertical_models:

Vertical Dynamics Models (post rig testing)
===========================================

Three commonly used models in the study of the vertical dynamic behavior of vehicles are introduced: the *quarter-car model* (:ref:`theory_quarter_car_model`), *half-car model* (:ref:`theory_half_car_model`), and the *full vertical car model* (:ref:`theory_full_car_model`).

The objective is to simulate the behavior of a specific vehicle by applying excitations that represent the vehicle traveling on a particular road at a certain speed. To accomplish this, the differential equations of various systems are derived and then solved numerically.


Determination of Differential Equations
---------------------------------------
Most studies and articles related to vertical vehicle models typically derive the motion's differential equations using Newton's equations. To provide a different perspective, we will derive the equations using *Lagrange's equations*. For this, we only need to define the kinetic energy $T$, dissipation energy $R$, and potential energy $V$.

All dynamic systems are defined with an equal number of generalized coordinates and degrees of freedom. The vector of generalized coordinates is given by

.. math::
   q = (q_1, q_2, ..., q_n)

and their derivatives are as 

.. math::
   \dot{q} = (\dot{q}_1, \dot{q}_2, ..., \dot{q}_n)

The Lagrangian is defined as the difference between the kinetic and potential energy of the system.

.. math::
  \mathcal{L} = T - V

The system equations, related to each degree of freedom, are given by the general Lagrange equation:

.. math::
   :label: lagrange_equation

   \frac{d}{dt} \left( \frac{\partial \mathcal{L}}{\partial \dot{q}_i} \right) - \frac{\partial \mathcal{L}}{\partial q_i} + \frac{\partial R}{\dot{\partial q}_i} = Q_i


Evaluating the above equation is necessary for each degree of freedom present in the system.

The goal is to obtain the dynamic response of the system, so static forces due to the weight of each element are not introduced into the equations.

Note that in all systems under study, potential energy is attributed to the energy stored in the springs, while kinetic energy is solely dependent on the derivatives of the generalized coordinates. The system to be explained will be represented in terms of kinetic energy ($T$) and potential energy ($V$), with a perturbation considered in the system. Consequently, we will assume $Q_i = 0$. Therefore, in this case, we can utilize a more practical equation:

.. math::
   \frac{d}{dt} \left( \frac{\partial T}{\partial \dot{q}_i} \right) + \frac{\partial V}{\partial q_i} + \frac{\partial R}{\partial \dot{q}_i} = 0

All the obtained equations are represented clearly, allowing for the consideration of other external forces simply.


Obtaining Natural Frequencies of the Systems
--------------------------------------------
To determine the natural frequencies of the systems, the obtained differential equations are linearized. It is assumed for all models that $\cos(\theta) = 1$ and $\sin(\theta) = \theta$, which is valid for small angle variations. The system of equations is represented in matrix format, allowing for the calculation of the mass $[M]$, damping $[C]$, and stiffness $[K]$ matrices.

With these matrices, it is possible to formulate an eigenvalue and eigenvector problem. This calculation is intended to provide an approximate value of the natural frequencies of the systems.

.. toctree::
   :maxdepth: 1

   quarter_car_model
   half_car_model
   full_car_model
